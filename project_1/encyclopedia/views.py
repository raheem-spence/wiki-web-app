from django import forms
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from markdown2 import Markdown

import random

from . import util

combined = '/t'.join(util.list_entries())

class NewEntry(forms.Form):
    title = forms.CharField(label="Title", widget=forms.TextInput(attrs={"placeholder": "Add Title"}))
    content = forms.CharField(widget=forms.Textarea(attrs={"placeholder": "Add Markdown content"}), label=False)

def index(request):
    markdowner = Markdown()
    if request.method == "POST":
        form_value = request.POST.get("q")
        if form_value in util.list_entries():
            return render(request, "encyclopedia/entry.html", {
            "entry": markdowner.convert(util.get_entry(form_value)),
            "title": form_value
            })
        if form_value in combined:
            entries = [s for s in util.list_entries() if form_value in s]
            return render(request, "encyclopedia/search.html", {
                "entries": entries
            })

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    markdowner = Markdown()
    return render(request, "encyclopedia/entry.html", {
        "entry": markdowner.convert(util.get_entry(title)),
        "title": title
    })

def new(request):
    markdowner = Markdown()
    if request.method == "POST":
        new_entry = NewEntry(request.POST)
        if new_entry.is_valid():
            title = new_entry.cleaned_data["title"]
            content = new_entry.cleaned_data["content"]

            if title in util.list_entries():
                messages.error(request, "Error: Entry already exists.")
                return render(request, "encyclopedia/new.html", {
                    "new_entry": NewEntry(),
                })

            util.save_entry(title, content)
            return render(request, "encyclopedia/entry.html", {
                "entry": markdowner.convert(util.get_entry(title)),
                "title": title
            })
    return render(request, "encyclopedia/new.html", {
        "new_entry": NewEntry(),
    })

def edit(request, edit):
    initial_entry =  {'title': edit, 'content': util.get_entry(edit)}
    markdowner = Markdown()
    if request.method == "POST":
        edited_entry = NewEntry(request.POST)
        if edited_entry.is_valid():
            title = edited_entry.cleaned_data["title"]
            content = edited_entry.cleaned_data["content"]

            util.save_entry(title, content)
            return render(request, "encyclopedia/entry.html", {
                "entry": markdowner.convert(util.get_entry(title)),
                "title": title
            })

    return render(request, "encyclopedia/edit.html", {
        "edit_entry": NewEntry(initial=initial_entry),
        "edit": edit
    })


def rand_entry(request):
    random_entry = random.choice(util.list_entries())
    return HttpResponseRedirect(reverse("title", args=[random_entry]))



from django.shortcuts import render, redirect
from markdown2 import markdown
from random import choice
from django import forms

from . import util


class NewEntryForm(forms.Form):
    entry_title = forms.CharField(label="Entry Title")
    entry_content = forms.CharField(
        widget=forms.Textarea, label="Entry Content")


class EditEntryForm(forms.Form):
    entry_content = forms.CharField(
        widget=forms.Textarea, label="Entry Content")


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def random(request):
    return get_page(request, choice(util.list_entries()))


def search(request):
    q = request.GET.get('q').strip()
    if q in util.list_entries():
        return redirect("title", title=q)
    return render(request, "encyclopedia/search.html", {"entries": util.search(q), "q": q})


def edit_page(request, title):
    content = util.get_entry(title.strip()).strip()

    ef = EditEntryForm(initial={'entry_content': content})

    if request.method == "POST":
        new_content = request.POST.get("entry_content").strip()
        util.save_entry(title, new_content)
        return redirect("title", title=title)

    if request.method == "GET":
        return render(request, "encyclopedia/edit.html", {
            "form": ef.as_p(),
            "content": content,
            "title": title
        })


def get_page(request, title):

    content = util.get_entry(title.strip())

    if content == None:
        error_msg = "Page Not Found."
        return render(request, "encyclopedia/error.html", {
            "title": title,
            "error_msg": error_msg
        })

    else:
        content = markdown(content)

        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": content
        })


def create(request):

    f = NewEntryForm()

    if request.method == "POST":
        # User form data
        fd = NewEntryForm(request.POST)

        if fd.is_valid():
            # Get title and content from cleaned form data
            title = fd.cleaned_data["entry_title"]
            content = fd.cleaned_data["entry_content"]
            entries = util.list_entries()

            if title in entries:
                error_msg = "An entry with this name already exists."
                error_title = "Entry Already Exists"
                return render(request, "encyclopedia/error.html", {
                    "title": title,
                    "error_msg": error_msg,
                    "error_title": error_title
                })

            # Use util function to save data into local storage
            util.save_entry(title, content)

            # Return to the newly created page
            return redirect("title", title=title)

        else:
            return render(request, "encyclopedia/create.html", {
                "form": fd
            })

    return render(request, "encyclopedia/create.html", {
        "form": f.as_p()
    })

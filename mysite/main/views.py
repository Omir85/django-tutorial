from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import ToDoList, Item
from .forms import CreateNewList

# Create your views here.
def index(response, id):
    ls = ToDoList.objects.filter(id = id)
    if ls:
        ls = ToDoList.objects.get(id = id)
    if response.method == "POST":
        print(response.POST)
        if response.POST.get("save"):
            for item in ls.item_set.all():
                if response.POST.get("c"+str(item.id)) == "clicked":
                    item.complete = True
                else:
                    item.complete = False
                item.save()
        elif response.POST.get("newItem"):
            text = response.POST.get("new")

            if len(text) > 2:
                ls.item_set.create(text=text, complete=False)
            else:
                print("Invalid")
    if ls:
        ls = ToDoList.objects.get(id=id)
        return render(response, "main/list.html", {"ls" : ls})
    else:
        return render(response, "main/base.html", {})

def home(response):
    return render(response, "main/home.html", {})

def create(response):
    if response.method == "POST":
        form = CreateNewList(response.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            t = ToDoList(name=name)
            t.save()
        return HttpResponseRedirect("/%i" %t.id)
    else:
        form = CreateNewList()
    return render(response, "main/create.html", {"form" : form})
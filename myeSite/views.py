from django.shortcuts import render

# Create your views here.
def main(request):
    type=request.GET.get("type", "")
    context = {
        "type":type
    }
    print(type)
    return render(request, 'main.html', context)

def loginModule(request):
    return render(request, 'myeSite/loginModule.html')

def signupModule(request):
    return render(request, 'myeSite/signupModule.html')

def fashionPage(request):
    return render(request, 'myeSite/fashionPage.html')


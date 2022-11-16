from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

def calculator_action(request):
    context = {}
    
    if(request.method == "GET"):
        context['top'] = 0
        context['middle'] = 0
        context['bottom'] = 0
        context['output'] = 0
        context['entering'] = "True"
        context['count'] = 1
        context['correct'] = False
        return render(request, './intro/calculator.html', context)
    
    if('button' not in request.POST):
        context['message'] = "Error"
        return render(request, './intro/error.html', context)

    if('top' not in request.POST):
        context['message'] = "Error"
        return render(request, './intro/error.html', context)
    
    if('bottom' not in request.POST):
        context['message'] = "Error"
        return render(request,'./intro/error.html', context)

    if('middle' not in request.POST):
        context['message'] = "Error"
        return render(request,'./intro/error.html', context)
    
    if('entering' not in request.POST):
        context['message'] = "Error"
        return render(request,'./intro/error.html', context)
    
    if('count' not in request.POST):
        context['message'] = "Error"
        return render(request,'./intro/error.html', context)

    if(request.POST['button'] not in ["plus", "minus", "times", "divide", "push","0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]):
        context['message'] = "Error"
        return render(request, './intro/error.html', context)
    
    try:
        val = int(request.POST['bottom'])
    except Exception as e:
        context['message'] = "Error"
        return render(request, './intro/error.html', context)

    try:
        val = int(request.POST['middle'])
    except Exception as e:
        context['message'] = "Error"
        return render(request, './intro/error.html', context)

    try:
        val = int(request.POST['top'])
    except Exception as e:
        context['message'] = "Error"
        return render(request, './intro/error.html', context)
    
    try:
        val = int(request.POST['count'])
    except Exception as e:
        context['message'] = "Error"
        return render(request, './intro/error.html', context)


    if( (not request.POST['entering'] == "True") and (not request.POST['entering'] == "False")):
        context['message'] = "Error"
        return render(request, './intro/error.html', context)

    if 'button' in request.POST:
        if(request.POST['button'].isdigit()):
            bottom = int(request.POST['bottom'])
            if(request.POST['entering'] == "True"):
                bottom = bottom * 10 + int(request.POST['button'])
                context['middle'] = request.POST['middle']
                context['top'] = request.POST['top']
                context['output'] = bottom
                context['bottom'] = bottom
                context['entering'] = "True"
                context['count'] = int(request.POST['count'])
                return render(request, './intro/calculator.html', context)

            else:
                context['entering'] = "True"
                context['top'] = request.POST['middle']
                context['middle'] = request.POST['bottom']
                bottom = int(request.POST['button'])
                context['bottom'] = bottom
                context['output'] = bottom
                context['count'] = int(request.POST['count']) + 1
                return render(request, './intro/calculator.html', context)

        elif(request.POST['button'] in ["plus", "minus", "times", "divide"]):
            print(request.POST['button'])
            if (int(request.POST['count']) < 2):
                context['message'] = "stack underflow"
                context['color'] = "red"
                return render(request,'./intro/error.html', context)

            context['middle'] = request.POST['top']
            context['top'] = 0
            bottom = int(request.POST['bottom'])
            middle = int(request.POST['middle'])
            result = 0
            if(request.POST['button'] == "plus"):
                result = bottom + middle
            elif(request.POST['button'] == "minus"):
                result = middle - bottom
            elif(request.POST['button'] == "times"):
                result = middle * bottom
            elif(request.POST['button'] == "divide"):
                if bottom == 0:
                    context['message'] = "divide by zero"
                    return render(request,'./intro/error.html', context)

                result = middle // bottom
            context['correct'] = True
            context['bottom'] = result
            context['output'] = result
            context['entering'] = "False"
            context['count'] = int(request.POST['count']) - 1
            return render(request, './intro/calculator.html', context)

        elif(request.POST['button'] == "push"):
            count = int(request.POST['count'])
            if(count >= 3):
                context['message'] = "stack overflow"
                return render(request,'./intro/error.html', context)                
            
            context['output'] = 0
            context['top'] = request.POST['middle']
            context['middle'] = request.POST['bottom']
            context['entering'] = "True"
            context['bottom'] = 0
            context['count'] = int(request.POST['count']) + 1
            return render(request, './intro/calculator.html', context)

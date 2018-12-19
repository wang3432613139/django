from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.template import loader
from django.shortcuts import render
from django.urls import reverse
from django.views import generic
from .models import Question,Choice
# Create your views here.
# def index(request):
#     return HttpResponse("""
#         <html>
#             <head>
#             </head>
#             <body>
#                 <h1>hello world</h1>
#             </body>
#         </html>
#     """)

# def index(request):
#
#     """
#     展示问题列表
#     :return:
#     """
#     question_list = Question.objects.all().order_by('-pub_date')[0:5]
#
#     # print(question_list)
#     # for q in question_list:
#     #     print(q.id,q.question_text,q.pub_date)
#     #     output=output+q.question_text
#     # print(output)
#
#     # print([q.question_text for q in question_list])
#     # output=','.join(q.question_text for q in question_list)
#     template = loader.get_template('polls/index.html')
#     context = {
#         'question_list':question_list
#     }
#     # return render_template('xx.html',q_list = q_list)
#     return HttpResponse(template())

def index(request):
    question_list = Question.objects.order_by('-pub_date1')[:5]
    context = {
        'question_list': question_list
    }
    print(
        1111
    )
    return render(request, 'polls/index.html', context)

def detail(request, question_id):

    """
    显示一个问题的详细信息，问题内容、问题发布时间、选项内容、每个选项投票数
    """
    # try:
    #     question = Question.objects.get(id=question_id)
    #
    #     # 写法1（基本思想）choices = Choice.objects.filter(question_id=question.id)
    #     # 由于orm代劳，question直接带出对应的choices
    #     # 写法2 choices = question.choice_set.all()
    #     # 由于前端模板语言本质是后端代码，可以吧上句话放html页面中写，有助于降低后端复杂度
    # except Question.DoesNotExist:
    #     raise Http404('404,此id的问题不存在')
    # print(question)
    # context = {
    #     'question':question,
    # }
    # 
    # return render(request,'polls/datail.html',context)
    try:
        question = Question.objects.get(id=question_id)
        print(question)

        # choices = Choice.objects.filter(question=question.id)
        # 由于orm 代劳， question 直接带出对应的choices
        # choices = question.choice_set.all()
        # 由于前端模板语言本质是后端代码，可以把上句话放在HTML页面中写，有助于降低后端复杂度
    except Question.DoesNotExist:
        raise Http404("404，此ID的问题不存在")
    print(question)
    context = {
        'question': question,
    }
    return render(request, 'polls/detail.html', context)
    # result_set = Question.objects.all().order_by('-pub_date'[0:5])
    #
    #
    # print(result_set)
    # question = get_object_or_404(Question,id=question_id)
    # return render(request,'polls/detail.html',{'question':question})
def results(request,question_id):
    """
    投票结果
    """
    question = Question.objects.get(id=question_id)
    return render(request,'polls/results.html',{'question':question})
def vote(request,question_id):

    """
    投票
    """
    try:
        question = Question.objects.get(id=question_id)
        choices = question.choice_set.all()
        choice_id = request.POST['choice']
        selected_choice = question.choice_set.get(id=choice_id)
    except Question.DoesNotExist as e:
        error_message = '问题内容不存在，检查问题id'
    except Choice.DoesNotExist as e:
        error_message = '问题对应的选项不存在'
        return render(request,'polls/detail.html',context={
            'question':question,
            'error_message':error_message
        })

    else:
        # sql update choice se votes=votes+1 where id=2
        selected_choice.votes +=1
        # commit;
        selected_choice.save()
        # 投票完重定向到 views.resuits(qid)
        return HttpResponseRedirect( reverse ('polls:detail',args=(question_id,)))
    print('hello world')
# 通过模板示例跟defindex类相比
class SimpleView(generic.ListView):
    template_engine = 'polls/index.html'
    context_object_name = 'question_list'

    def get_queryset(self):
        return Question.objects.all()
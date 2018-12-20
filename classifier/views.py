from django.http import HttpResponse
from .models import Img
from django.template import loader
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from .forms import ImgUpdateForm
from django.contrib.auth.models import User


# Create your views here.
def index(request):
    classification_types = Img.CLASSIFICATION_TYPES
    class_list = [i[1] for i in classification_types]
    template = loader.get_template('classifier/index.html')
    context = {
        'classification_list': class_list,
    }
    return HttpResponse(template.render(context, request))


def classify_home(request):
    try:
        classification_types = Img.CLASSIFICATION_TYPES
        class_list = [i[1] for i in classification_types]
        img_objs_to_classify = [i for i in Img.objects.all() if not i.image_classification]
        first_img_obj = img_objs_to_classify[0].id
        template = loader.get_template('classifier/classify_imgs.html')
        context = {
            'classification_list': class_list,
            'next_item_to_classify': first_img_obj,
        }
        return HttpResponse(template.render(context, request))
    except IndexError:
        template = loader.get_template('classifier/success.html')
        return HttpResponse(template.render({}, request))


def classify_iter(request, img_id):

    # need to change this to class based views in order to do the post easier
    classification_types = Img.CLASSIFICATION_TYPES
    class_list = [i[0] for i in classification_types]
    # template = loader.get_template('classifier/classify_imgs_iter.html')
    template = loader.get_template('classifier/img_update_form.html')
    img_obj = get_object_or_404(Img, pk=img_id)

    if request.method == 'POST':
        form = ImgUpdateForm(request.POST, instance=img_obj)
        if form.is_valid():
            print(form.cleaned_data['image_classification'])
            print(request.user.username)
            form.instance.updated_by_user = request.user.username
            form.save()
            next_img = Img.objects.filter(image_classification='').first()
            if next_img:
                return redirect('classify_iter', img_id=next_img.id)
            if not next_img:
                template = loader.get_template('classifier/success.html')
                return HttpResponse(template.render({}, request))

    else:
        form = ImgUpdateForm()

    context = {
        'classification_list': class_list,
        'first_item': img_obj,
        'form':form,
    }

    return HttpResponse(template.render(context, request))


def summary(request):
    imgs = Img.objects.all()
    num_classified = len([i for i in imgs if i.image_classification])
    num_total = len([i for i in imgs])
    img_count_dict = {i[0]:0 for i in Img.CLASSIFICATION_TYPES}
    users = {i.updated_by_user for i in imgs}
    user_count_dict = {i:0 for i in users}
    img_count_dict[''] = 0
    for img in imgs:
        img_count_dict[img.image_classification] += 1
        if img.image_classification:
            user_count_dict[img.updated_by_user] += 1
    # replace the empty one
    img_count_dict['not classified'] = img_count_dict.pop("")
    user_percent_count_dict = {i:[
                                user_count_dict[i],
                                "{0:.0%}".format(user_count_dict[i]/num_total),
                                User.objects.get(username=i).last_login if i != '' else 'n/a'] for i in user_count_dict
                                }

    template = loader.get_template('classifier/summary.html')
    context = {
        'num_classified': num_classified,
        'num_total': num_total,
        'img_count_dict': img_count_dict.items(),
        'users': user_count_dict.items(),
        'user_with_percent': user_percent_count_dict.items(),
    }
    return HttpResponse(template.render(context, request))


def profile(request):
    template = loader.get_template('classifier/profile.html')
    if request.user.is_authenticated:
        user = request.user.username
        first_name = request.user.first_name
        last_name = request.user.last_name
        email = request.user.email
        context = {
            'username':user,
            'first_name':first_name,
            'last_name':last_name,
            'email':email,
        }
        return HttpResponse(template.render(context, request))
    else:
        return HttpResponse(template.render({}, request))


def review(request):
    template = loader.get_template('classifier/review.html')
    classification_types = Img.CLASSIFICATION_TYPES
    class_list = [i[0] for i in classification_types]
    imgs = [i for i in Img.objects.all()]
    context = {
        'classification_list': class_list,
        'imgs': imgs,
    }
    return HttpResponse(template.render(context, request))
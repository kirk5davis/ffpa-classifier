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
    model_types = Img.WA_LANDSCAPE_MODEL_TYPE
    class_list = [i[1] for i in classification_types]
    model_list = [i[1] for i in model_types]
    template = loader.get_template('classifier/index.html')
    context = {
        'classification_list': class_list,
        'model_list': model_list,
    }
    return HttpResponse(template.render(context, request))


def classify_home(request):
    west_finished = None
    east_finished = None
    classification_types = Img.CLASSIFICATION_TYPES
    class_list = [i[1] for i in classification_types]
    try:
        next_img_obj_to_classify_west = Img.objects.filter(image_classification='', model_type='WESTSIDE').first().id
    except (IndexError, AttributeError) as west_finished:
        next_img_obj_to_classify_west = None
    try:
        next_img_obj_to_classify_east = Img.objects.filter(image_classification='', model_type='EASTSIDE').first().id
    except (IndexError, AttributeError) as east_finished:
        next_img_obj_to_classify_east = None
    if west_finished and east_finished:
        template = loader.get_template('classifier/success.html')
        return HttpResponse(template.render({}, request))
    
    template = loader.get_template('classifier/classify_imgs.html')
    context = {
        'classification_list': class_list,
        'next_item_to_classify_west': next_img_obj_to_classify_west, 
        'next_item_to_classify_east': next_img_obj_to_classify_east,
    }
    return HttpResponse(template.render(context, request))
        


def classify_iter(request, model_type, img_id):

    # need to change this to class based views in order to do the post easier
    classification_types = Img.CLASSIFICATION_TYPES
    class_list = [i[0] for i in classification_types]
    # template = loader.get_template('classifier/classify_imgs_iter.html')
    template = loader.get_template('classifier/img_update_form.html')
    img_obj = get_object_or_404(Img, pk=img_id, model_type=model_type)

    if request.method == 'POST':
        form = ImgUpdateForm(request.POST, instance=img_obj)
        if form.is_valid():
            print(form.cleaned_data['image_classification'])
            print(request.user.username)
            form.instance.updated_by_user = request.user.username
            form.save()
            next_img = Img.objects.filter(image_classification='', model_type=model_type).first()
            if next_img:
                return redirect('classify_iter', img_id=next_img.id, model_type=next_img.model_type)
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
    model_types = [i[1] for i in Img.WA_LANDSCAPE_MODEL_TYPE]
    imgs_east = [i for i in Img.objects.all() if i.image_classification and i.model_type == 'EASTSIDE']
    imgs_west = [i for i in Img.objects.all() if i.image_classification and i.model_type == 'WESTSIDE']
    context = {
        'classification_list': class_list,
        'imgs_east': imgs_east,
        'imgs_west': imgs_west,
    }
    return HttpResponse(template.render(context, request))

def success(request):
    template = loader.get_template('classifier/success.html')
    return HttpResponse(template.render({}, request))
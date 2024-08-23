from django.shortcuts import render, redirect, get_object_or_404
from FINALApp.models import *
from django.utils import timezone
from django.contrib import messages
from .models import user 
from django.http import HttpResponseNotAllowed
# HttpResponse, JsonResponse

# Create your views here.
def index(request):
    return render(request, 'index.html')

def adminlogin(request):
    if request.method == "GET":
        return render(request, 'adminlogin.html')
    elif request.method == "POST":
        aname = request.POST.get("aname", None)
        apassword = request.POST.get("apassword", None)
        if aname == "admin" and apassword == "admin":
            context = {"login_success": True}
            return render(request, 'adminlogin.html', context)
        else:
            context = {"login_failed": True}
            return render(request, 'adminlogin.html', context)
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])




# def admindash(request):
#     total_users = user.objects.count()
#     total_videos = Video.objects.count()
#     total_events = Event.objects.count()

#     context = {
#         'total_users': total_users,
#         'total_videos': total_videos,
#         'total_events': total_events,
#     }
#     return render(request, 'admindash.html')

from django.db.models.functions import TruncMonth
def admindash(request):
    total_users = user.objects.count()
    total_videos = Video.objects.count()
    total_events = Event.objects.count()
    total_complaints = Complaint.objects.count()


    # Get the number of events per month for the current year
    now = timezone.now()
    events_per_month = (
        Event.objects
        .filter(event_date__year=now.year)
        .annotate(month=TruncMonth('event_date'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )

    months = []
    counts = []
    for event in events_per_month:
        months.append(event['month'].strftime('%B'))  # Get the month name
        counts.append(event['count'])

    # Get events from the previous year
    last_year = now.year - 1
    previous_year_events = Event.objects.filter(event_date__year=last_year)

    context = {
        'total_users': total_users,
        'total_videos': total_videos,
        'total_events': total_events,
        'total_complaints': total_complaints,
        'events': Event.objects.all(),
        'months': months,
        'counts': counts,
        'previous_year_events': previous_year_events,  # Add previous year events to context
    }

    return render(request, 'admindash.html', context)




def addevents(request):
    return render(request, 'addevents.html')

def saveevent(request):
    if request.method == "POST":
        event_name = request.POST.get('event_name')
        event_date = request.POST.get('event_date')
        event_time = request.POST.get('event_time')
        event_details = request.POST.get('event_details')
        event_image = request.FILES.get('event_image')

        # Save the event details to the database
        event = Event(event_name=event_name, event_date=event_date, event_time=event_time, event_details=event_details, event_image=event_image)
        event.save()
        return render(request, 'addevents.html')
    return render(request, 'addevents.html')

def editevent(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    
    if request.method == 'POST':
        event.event_name = request.POST.get('event_name')
        event.event_date = request.POST.get('event_date')
        event.event_time = request.POST.get('event_time')
        event.event_details = request.POST.get('event_details')
        event.event_image = request.FILES.get('event_image')
        event.save()
        return redirect('/upcomingevents/')
    
    return render(request, 'editevent.html', {'event': event})


# def deleteevent(request, event_id):
#     if request.method == "POST":
#         event_instance = get_object_or_404(Event, id=event_id)
#         event_instance.delete()
#         return redirect('/upcomingevents/')  # Make sure this URL is correct and points to the page listing the users
#     else:
#         return HttpResponseNotAllowed(['POST'])    

def deleteevent(request, id):
    if request.method == "POST":
        event_instance = get_object_or_404(Event, id=id)
        event_instance.delete()
        return redirect('/upcomingevents/')  # Make sure this URL is correct and points to the page listing the users
    else:
        return HttpResponseNotAllowed(['POST'])  


def upcomingevents(request):
    today = timezone.now().date()
    upcoming_events = Event.objects.filter(event_date__gte=today)
    return render(request, 'upcomingevents.html', {'events': upcoming_events})

from django.shortcuts import get_object_or_404, redirect


def completedevents(request):
    today = timezone.now().date()
    completed_events = Event.objects.filter(event_date__lt=today)
    return render(request, 'completedevents.html', {'events': completed_events})


def viewevents(request):
    return render(request, 'viewevents.html')


def videogallery(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        video_file = request.FILES.get('video_file')
        
        thumbnail = request.FILES.get('thumbnail')  # Retrieve thumbnail file

        # Create a new Video object and save to database
        video = Video(title=title, description=description, video_file=video_file, thumbnail=thumbnail)
        video.save()

        # Redirect to a success page or render a success message
        return render(request, 'videogallery.html')  # Replace 'success-url' with your actual success URL or view name

    # Fetch all videos to display in the gallery section
    videos = Video.objects.all()
    return render(request, 'videogallery.html', {'videos': videos})

def editvideogallery(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    
    if request.method == 'POST':
        video.title = request.POST.get('title')
        
        video.description = request.POST.get('description')
        video.video_file = request.FILES.get('video_file')
        
        video.thumbnail = request.FILES.get('thumbnail')
        video.save()
        return redirect('/videogallery/')
    
    return render(request, 'editvideogallery.html', {'video': video})

def deletevideogallery(request, id):
    if request.method == "POST":
        video_instance = get_object_or_404(Video, id=id)
        video_instance.delete()
        return redirect('/videogallery/')  # Make sure this URL is correct and points to the page listing the users
    else:
        return HttpResponseNotAllowed(['POST'])  






def flashnews(request):
    if request.method == 'POST':
        flash_news = request.POST.get('admin_flash')
        if flash_news:
            # Save the flash news to the database
            FlashNews.objects.create(admin_flash=flash_news)

            return redirect('flashnews') 

    # Fetch all flash news from the database
    flashnews = FlashNews.objects.all().order_by('-created_at')  # You might want to order by date

    return render(request, 'flashnews.html', {'flashnews': flashnews})


from django.db.models import Count
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from .models import Complaint

from django.shortcuts import render, get_object_or_404, redirect
from .models import Complaint
from django.urls import reverse

def complaints(request):
    # Aggregate complaint counts by apartment_number
    complaints = Complaint.objects.values('apartment_number').annotate(total_complaints=Count('id')).order_by('apartment_number')

    # Create a dictionary to hold complaint counts for each apartment
    complaint_data = {complaint['apartment_number']: complaint['total_complaints'] for complaint in complaints}

    # Ensure all 10 apartments are represented in the dictionary
    apartments = []
    for i in range(1, 11):
        apartments.append({
            'apartment_number': i,
            'total_complaints': complaint_data.get(i, 0)
        })

    context = {
        'apartments': apartments,
    }

    return render(request, 'complaints.html', context)

def admin_complaints(request, apartment_number):
    complaints = Complaint.objects.filter(apartment_number=apartment_number)

    if request.method == "POST":
        # Handle the form submission here
        complaint_id = request.POST.get('complaint_id')
        amount = request.POST.get('amount')
        bill_image = request.FILES.get('bill_image')
        username = request.POST.get('name')
        # process other fields accordingly

        complaint = get_object_or_404(Complaint, id=complaint_id)

        complaint.amount = amount
        if bill_image:
            complaint.bill_image = bill_image
        complaint.save()

        # Perform necessary actions with the submitted data
        messages.success(request, 'Fee request submitted successfully!')

    context = {
        'apartment_number': apartment_number,
        'complaints': complaints,
    }
    return render(request, 'admin_complaints.html', context)



# def feecomplaint(request, pk):
#     complaint_instance = get_object_or_404(Complaint, id=pk)
#     return render(request, 'feecomplaint.html', {'complaint':  complaint_instance})


def members(request):
    userdetails = user.objects.all()
    return render(request, 'members.html', {'users': userdetails})


def deleteuserview(request, id):
    if request.method == "POST":
        user_instance = get_object_or_404(user, id=id)
        user_instance.delete()
        return redirect('/members/')  # Make sure this URL is correct and points to the page listing the users
    else:
        return HttpResponseNotAllowed(['POST'])    

def inactivatebtn(request):
    userid=request.GET["userid"]
    user.objects.filter(id=userid).update(is_active=0)
    userdetails=user.objects.all()
    return render(request,'members.html',{'users':userdetails})

def activatebtn(request):
    userid=request.GET["userid"]
    user.objects.filter(id=userid).update(is_active=1)
    userdetails=user.objects.all()
    return render(request,'members.html',{'users':userdetails})    

def view_payments(request):
    payments = Payment.objects.all()
    return render(request, 'view_payments.html', {'payments': payments})



#user


def userregister(request):
    return render(request, 'userregister.html')


def savenewuser(request):
    if request.method == 'POST':
        username = request.POST["username"]
        contact = request.POST["contact"]
        apartment_number = request.POST["apartment_number"]
        housing_status = request.POST["housing_status"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]

        

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'userregister.html')

        # Check if the contact number is already registered
        if user.objects.filter(contact=contact).exists():
            messages.error(request, "This contact number is already registered.")
            return render(request, 'userregister.html')

        # Create new user instance
        new_user = user(username=username, contact=contact, apartment_number=apartment_number,
                        housing_status=housing_status, password=password, is_active=0)
        new_user.save()

        # Redirect to login page with a success message
        messages.success(request, "User registered successfully.")
        return redirect('userlogin')

    return render(request, 'userregister.html')

def userlogin(request):
    if request.method == 'POST':
        contact = request.POST.get('contact')
        password = request.POST.get('password')
        
        try:
            user_instance = user.objects.get(contact=contact)
            
            if user_instance.password == password:
                if user_instance.is_active:
                    request.session['user_id'] = user_instance.id
                    request.session['user_contact'] = user_instance.contact  # Store contact in session
                    return redirect('userhome')
                else:
                    messages.error(request, 'User is not active. Please contact admin.')
                    return render(request, 'userlogin.html')
            else:
                messages.error(request, 'Incorrect password.')
                return render(request, 'userlogin.html')
        
        except user.DoesNotExist:
            messages.error(request, 'User does not exist.')
            return render(request, 'userlogin.html')
    
    return render(request, 'userlogin.html')



def userhome(request):
    user_id = request.session.get('user_id')
    if user_id:
        user_instance = user.objects.get(id=user_id)
        flashnews = FlashNews.objects.latest('created_at')
        total_events = Event.objects.count()
        total_videos = Video.objects.count()
        
        # Count the total complaints for the logged-in user
        total_complaints = Complaint.objects.filter(user=user_instance).count()
        total_payments = Payment.objects.filter(user=user_instance).count()
        
        context = {
            'username': user_instance.username,
            'contact': user_instance.contact,
            'apartment_number': user_instance.apartment_number,
            'housing_status': user_instance.housing_status,
            'flashnews': flashnews,
            'total_events': total_events,
            'total_videos': total_videos,
            'total_complaints': total_complaints,  # Add the total_complaints to the context
            'total_payments': total_payments,  # Add the total_payments to the context
        }
        return render(request, 'userhome.html', context)
    else:
        return redirect('userlogin')




def forgotpasswordview(request):
    return render(request, 'forgotpassword.html')


def passwordrequestview(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        contact = request.POST.get('contact')

        try:
            user_instance = user.objects.get(username=username, contact=contact)
            # Store user ID in session to identify the user in the password change view
            request.session['user_id'] = user_instance.id
            return redirect('change_password')
        except user.DoesNotExist:
            messages.error(request, 'User not found')
            return redirect('forgotpassword')

    return render(request, 'userlogin.html')




def change_password(request):
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, 'Session expired. Please request a password reset again.')
        return redirect('forgotpassword')

    user_instance = user.objects.get(id=user_id)

    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        user_instance.password = new_password  # This should ideally hash the password
        user_instance.save()

        # Clear the session
        del request.session['user_id']

        messages.success(request, 'Password changed successfully')
        return redirect('userlogin')

    return render(request, 'change_password.html', {'user': user_instance, 'old_password': user_instance.password })



def userupcomingevents(request):
    today = timezone.now().date()
    upcoming_events = Event.objects.filter(event_date__gte=today)
    return render(request, 'userupcomingevents.html', {'events': upcoming_events})

def usercompletedevents(request):
    today = timezone.now().date()
    completed_events = Event.objects.filter(event_date__lt=today)
    return render(request, 'usercompletedevents.html', {'events': completed_events})

def usergallery(request):
    videos = Video.objects.all()
    return render(request, 'usergallery.html', {'videos': videos})


def usercomplaints(request):
    return render(request, 'usercomplaints.html')




def savecomplaints(request):
    if request.method == 'POST':
        category = request.POST.get("category")
        title = request.POST.get("title")
        description = request.POST.get("description")
        image = request.FILES.get("image", None)

        user_id = request.session.get('user_id')
        if user_id:
            user_instance = user.objects.get(id=user_id)
            
            # Save the complaint with the linked user and include the user's name and contact number
            save_complaint = Complaint(
                user=user_instance,
                username=user_instance.username,
                contact=user_instance.contact,
                apartment_number= user_instance.apartment_number,
                housing_status=user_instance.housing_status,
                category=category,
                title=title,
                description=description,
                image=image
                
            )
            save_complaint.save()

            messages.success(request, "Complaint registered successfully.")
            return redirect('usercomplaints')
        else:
            messages.error(request, "User is not logged in.")
            return redirect('userlogin')

    return render(request, 'usercomplaints.html')


def previewcomplaint(request):
    # Retrieve the user_id from the session
    user_id = request.session.get('user_id')
    
    if user_id:
        # Fetch the user instance
        user_instance = user.objects.get(id=user_id)
        
        # Fetch complaints associated with the user instance
        complaint_data = Complaint.objects.filter(user=user_instance)
        
        # Render the complaints in the view_complaint.html template
        return render(request, 'view_complaint.html', {'Complaint_data': complaint_data})
    else:
        # Redirect to login if the user is not logged in
        messages.error(request, "User is not logged in.")
        return redirect('userlogin')


def mark_as_done(request, complaint_id):
    complaint = get_object_or_404(Complaint, id=complaint_id)
    complaint.status = 'Done'
    complaint.save()
    return redirect('admin_complaints', apartment_number=complaint.apartment_number)



from django.shortcuts import render, redirect
from django.urls import reverse
import uuid
from .models import Payment

def dummy_payment_view(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return render(request, 'dummy_payment.html', {'error': 'User not logged in'})

    user_instance = user.objects.get(id=user_id)
    user_payments = Payment.objects.filter(user=user_instance)

    if request.method == 'POST':
        try:
            amount = float(request.POST.get('amount', '2000'))  # Get the amount from POST data
            transaction_id = str(uuid.uuid4())  # Generate a unique transaction ID
            upi_id = request.POST.get('upi_id')

            # Create a new payment record
            Payment.objects.create(
                user=user_instance,
                username=user_instance.username,
                apartment_number=user_instance.apartment_number,
                housing_status=user_instance.housing_status,
                amount=amount,
                status='Completed',  # Set this based on actual payment status
                transaction_id=transaction_id,
                upi_id = upi_id
                
            )

            return redirect('payment_success')  # Redirect to a success page to prevent form resubmission
        except Exception as e:
            return render(request, 'dummy_payment.html', {
                'error': str(e),
                'user_instance': user_instance,
                'user_payments': user_payments,
            })

    return render(request, 'dummy_payment.html', {
        'user_instance': user_instance,
        'user_payments': user_payments,
    })


def payment_success(request):
    return render(request, 'payment_success.html')


def view_transaction(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    
    return render(request, 'view_transaction.html', {'payment': payment})


from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from weasyprint import HTML
from django.template.loader import render_to_string
from .models import Payment

from django.templatetags.static import static
from django.utils.http import urlquote

def payment_pdf_view(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    logo_url = request.build_absolute_uri(static('images/HomEase_logo.png'))
    context = {
        'payment': payment,
        'logo_url': logo_url,
    }
    html_content = render_to_string('payment_details_pdf.html', context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="payment_{payment_id}.pdf"'
    HTML(string=html_content).write_pdf(response)
    return response




from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import Chat, user
from django.http import JsonResponse

@csrf_exempt
def user_chat(request):
    # Assume the admin name is 'President'
    to_user = 'President'
    from_user = request.session.get('user_contact')  # Get the user's contact from the session
    
    # Fetch chat history
    chats = Chat.objects.filter(
        (models.Q(from_user=from_user, to_user=to_user) | models.Q(from_user=to_user, to_user=from_user))
    ).order_by('timestamp')
    
    # Pass the recipient's name in the session
    request.session['to_user'] = to_user
    
    context = {
        'chats': chats,
        'to_user': to_user,
        'user_name': request.session.get('user_name')  # User's name for display
    }
    
    return render(request, 'user_chat.html', context)

@csrf_exempt
def admin_chat(request):
    # Fetch all users
    users = user.objects.all()
    
    # Handle selected user chat
    to_user = request.GET.get('user')
    chats = None
    
    if to_user:
        from_user = 'President'
        chats = Chat.objects.filter(
            (models.Q(from_user=from_user, to_user=to_user) | models.Q(from_user=to_user, to_user=from_user))
        ).order_by('timestamp')
        
        # Pass the selected user's contact in the session
        request.session['to_user'] = to_user
    
    context = {
        'users': users,
        'chats': chats,
        'selected_user': to_user
    }
    
    return render(request, 'admin_chat.html', context)

@csrf_exempt
def send_chat(request):
    if request.method == 'POST':
        from_user = request.session.get('user_contact')  # Get the contact from the session for the sender
        if not from_user:
            return JsonResponse({'status': 'error', 'message': 'User not authenticated'}, status=401)

        to_user = request.POST.get('to_user')
        chat_message = request.POST.get('chat')

        if not to_user or not chat_message:
            return JsonResponse({'status': 'error', 'message': 'Missing to_user or chat message'}, status=400)

        # Create a new chat message
        new_chat = Chat.objects.create(
            from_user=from_user,
            to_user=to_user,
            chat=chat_message,
        )
        return JsonResponse({'status': 'success'}, status=201)
    
@csrf_exempt
def get_chats(request):
    if request.method == 'POST':
        from_user = request.POST.get('from_user')
        to_user = request.POST.get('to_user')

        if not from_user or not to_user:
            return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

        # Retrieve the chat messages between these two users
        chats = Chat.objects.filter(from_user=from_user, to_user=to_user) | Chat.objects.filter(from_user=to_user, to_user=from_user)
        
        # Return a list of chat messages with sender information
        chat_list = list(chats.values('id', 'from_user', 'to_user', 'chat', 'created_at'))
        
        return JsonResponse(chat_list, safe=False)    



# from django.shortcuts import render, get_object_or_404
# from django.http import JsonResponse
# from .models import ChatMessage, user, admin

# def chat_view(request):
#     current_user = request.user

#     # Check if the current user is a user (instance of the user model)
#     if user.objects.filter(id=current_user.id).exists():
#         admins = admin.objects.all()
#         return render(request, 'chat.html', {'contacts': admins, 'current_user': current_user})
    
#     # Check if the current user is an admin (instance of the admin model)
#     elif admin.objects.filter(id=current_user.id).exists():
#         users = user.objects.all()
#         return render(request, 'chat.html', {'contacts': users, 'current_user': current_user})
    
#     # Handle cases where the current user is neither a user nor an admin
#     else:
#         return render(request, 'chat.html', {'contacts': [], 'current_user': current_user})

# def get_chats(request):
#     if request.method == "POST":
#         from_user_id = request.POST.get('from_user')
#         to_user_id = request.POST.get('to_user')
#         from_admin_id = request.POST.get('from_admin')
#         to_admin_id = request.POST.get('to_admin')

#         if from_user_id and to_admin_id:
#             messages = ChatMessage.objects.filter(
#                 (models.Q(from_user_id=from_user_id) & models.Q(to_admin_id=to_admin_id)) |
#                 (models.Q(from_user_id=to_admin_id) & models.Q(to_admin_id=from_user_id))
#             ).order_by('timestamp')
#         elif from_admin_id and to_user_id:
#             messages = ChatMessage.objects.filter(
#                 (models.Q(from_admin_id=from_admin_id) & models.Q(to_user_id=to_user_id)) |
#                 (models.Q(from_admin_id=to_user_id) & models.Q(to_user_id=from_admin_id))
#             ).order_by('timestamp')
#         else:
#             messages = []

#         # Returning chat messages as JSON
#         return JsonResponse([{
#             'from_user': msg.from_user.username if msg.from_user else '',
#             'to_user': msg.to_user.username if msg.to_user else '',
#             'from_admin': msg.from_admin.name if msg.from_admin else '',
#             'to_admin': msg.to_admin.name if msg.to_admin else '',
#             'message': msg.message,
#             'timestamp': msg.timestamp
#         } for msg in messages], safe=False)
    

# def send_chat(request):
#     if request.method == "POST":
#         from_user_id = request.POST.get('from_user')
#         to_user_id = request.POST.get('to_user')
#         from_admin_id = request.POST.get('from_admin')
#         to_admin_id = request.POST.get('to_admin')
#         message = request.POST.get('chat')

#         # Storing chat message in the database
#         if from_user_id and to_admin_id:
#             from_user = get_object_or_404(user, id=from_user_id)
#             to_admin = get_object_or_404(admin, id=to_admin_id)
#             chat_message = ChatMessage.objects.create(
#                 from_user=from_user,
#                 to_admin=to_admin,
#                 message=message
#             )
#         elif from_admin_id and to_user_id:
#             from_admin = get_object_or_404(admin, id=from_admin_id)
#             to_user = get_object_or_404(user, id=to_user_id)
#             chat_message = ChatMessage.objects.create(
#                 from_admin=from_admin,
#                 to_user=to_user,
#                 message=message
#             )

#         # Response after successfully storing the message
#         return JsonResponse({'status': 'success', 'message': chat_message.message})

#     # Fallback for non-POST requests
#     return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


# views.py

# from django.shortcuts import render, get_object_or_404
# from django.http import JsonResponse
# from .models import user, ChatMessage

# def chat_view(request):
#     current_user = request.user  # Assuming you have a way to get the current user
#     users = user.objects.exclude(id=current_user.id)  # Get all users except the current one
#     return render(request, 'chat.html', {'users': users})

# def get_chats(request):
#     if request.method == "POST":
#         from_user_id = request.POST.get('from_user')
#         to_user_id = request.POST.get('to_user')
#         from_user = get_object_or_404(user, id=from_user_id)
#         to_user = get_object_or_404(user, id=to_user_id)

#         messages = ChatMessage.objects.filter(
#             (models.Q(from_user=from_user) & models.Q(to_user=to_user)) |
#             (models.Q(from_user=to_user) & models.Q(to_user=from_user))
#         ).order_by('timestamp')

#         return JsonResponse([{
#             'from_user': msg.from_user.username,
#             'to_user': msg.to_user.username,
#             'message': msg.message,
#             'timestamp': msg.timestamp
#         } for msg in messages], safe=False)

# def send_chat(request):
#     if request.method == "POST":
#         from_user_id = request.POST.get('from_user')
#         to_user_id = request.POST.get('to_user')
#         message = request.POST.get('chat')

#         from_user = get_object_or_404(user, id=from_user_id)
#         to_user = get_object_or_404(user, id=to_user_id)

#         chat_message = ChatMessage.objects.create(
#             from_user=from_user,
#             to_user=to_user,
#             message=message
#         )
#         return JsonResponse({'status': 'success', 'message': chat_message.message})

# from django.shortcuts import render, redirect


# def user_chat_view(request, user_id):
#     user = user.objects.get(id=user_id)
#     admin = admin.objects.first()  # Assuming only one admin, modify as needed

#     if request.method == 'POST':
#         message = request.POST.get('message')
#         if message:
#             ChatMessage.objects.create(sender=user, receiver=admin, message=message)
#         return redirect('user_chat', user_id=user.id)

#     chats = ChatMessage.objects.filter(sender=user) | ChatMessage.objects.filter(receiver=user)
#     return render(request, 'user_chat.html', {'user': user, 'admin': admin, 'chats': chats})

# from django.shortcuts import render, redirect
# from .models import ChatMessage, user, admin

# def admin_chat_view(request):
#     admin_instance = admin.objects.first()  # Retrieve the first admin instance
    
#     if not admin_instance:
#         return render(request, 'error.html', {'message': 'No admin found. Please set up an admin account.'})
    
#     users = user.objects.all()
    
#     if request.method == 'POST':
#         user_id = request.POST.get('user_id')
#         message = request.POST.get('message')
#         user_instance = user.objects.get(id=user_id)
#         if message:
#             ChatMessage.objects.create(sender=user_instance, receiver=admin_instance, message=message)
#         return redirect('admin_chat')

#     user_id = request.GET.get('user_id')
#     if user_id:
#         selected_user = user.objects.get(id=user_id)
#         chats = ChatMessage.objects.filter(sender=selected_user) | ChatMessage.objects.filter(receiver=selected_user)
#     else:
#         selected_user = None
#         chats = None

#     return render(request, 'admin_chat.html', {'admin': admin_instance, 'users': users, 'selected_user': selected_user, 'chats': chats})


# from django.shortcuts import render, redirect
# from django.contrib import messages
# from .models import MaintenanceFee


# def maintenance_fee_list(request):
#     # Assume the user ID is stored in the session or obtained through some other mechanism
#     user_id = request.session.get('user_id')  # Or use another method to get the current user's ID

#     if user_id:
#         try:
#             user_instance = user.objects.get(id=user_id)
#             maintenance_fees = MaintenanceFee.objects.filter(user=user_instance)
            
#             # Render the page with maintenance fees
#             return render(request, 'maintenance_fee_list.html', {'maintenance_fees': maintenance_fees})
#         except user.DoesNotExist:
#             messages.error(request, "User does not exist.")
#             return redirect('userlogin')  # Redirect to login or home if user does not exist
#         except MaintenanceFee.DoesNotExist:
#             messages.error(request, "No maintenance fee records found.")
#             return render(request, 'maintenance_fee_list.html', {'maintenance_fees': []})  # Render with empty list
#     else:
#         messages.error(request, "User is not logged in.")
#         return redirect('userlogin')  # Redirect to login page or any other appropriate page
    


# def maintenance_fee_admin_list(request):
#     try:
#         maintenance_fees = MaintenanceFee.objects.all()
#         return render(request, 'maintenance_fee_admin_list.html', {'maintenance_fees': maintenance_fees})
#     except MaintenanceFee.DoesNotExist:
#         messages.error(request, "No maintenance fee records found.")
#         return render(request, 'maintenance_fee_admin_list.html', {'maintenance_fees': []})    




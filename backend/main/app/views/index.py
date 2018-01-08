from app import app, jinja, logger
from app.modules import db, mqtt as Mqtt 
from sanic.response import json, redirect
from sanic import Blueprint
import asyncio
from threading import Thread


def Thread_pub(loop, message, topic):
    asyncio.set_event_loop(loop)
    client = Mqtt.mqtt()
    loop.run_until_complete(client.publish(message, topic))




bp_index = Blueprint('bp_index')

@bp_index.route('/')
@app.auth.login_required
async def index(request):
    user_amount = db.User.objects.count()
    users = db.User.objects
    return jinja.render('index.html', **locals())

@bp_index.route('/IOT')
@app.auth.login_required
async def IOT(request):
    IOT_amount = db.IOT.objects.count()
    IOTS = db.IOT.objects
    return jinja.render('IOT.html', **locals())

@app.route('/lock/<number:int>', methods=['GET'])
@app.auth.login_required
async def lock(request, number):
    try:
        IOT = db.IOT.objects.get(number=number)
        IOT.is_used = True
        IOT.last_user = 'SYSTEM'
        IOT.save()
        message = {
                'error_request': False,
                'method': 'SYSTEM',
                'locked': True,
                'uid': 'SYSTEM_LOCK'
                } 
        topic = "$SYS/"+str(number)
        new_loop = asyncio.new_event_loop()
        t = Thread(target=Thread_pub, args=(new_loop,message, topic))
        t.start()
        t.join()
        return redirect('/IOT')
    except:
        return redirect('/IOT')

@app.route('/unlock/<number:int>', methods=['GET'])
@app.auth.login_required
async def unlock(request, number):
    try:
        IOT = db.IOT.objects.get(number=number)
        if IOT.last_user == 'SYSTEM' and IOT.is_used:
            IOT.is_used = False
            message = {
                'error_request': False,
                'method': 'SYSTEM',
                'locked': False,
                } 
            topic = "$SYS/"+str(number)
            new_loop = asyncio.new_event_loop()
            t = Thread(target=Thread_pub, args=(new_loop,message, topic))
            t.start()
            t.join()
            IOT.save()
        elif IOT.is_used:
            user = db.User.objects.get(email=IOT.last_user)
            user.is_used = False
            IOT.is_used = False
            message = {
                'error_request': False,
                'method': 'SYSTEM',
                'locked': False,
                } 
            
            topic = "$SYS/"+str(number)
            new_loop = asyncio.new_event_loop()
            t = Thread(target=Thread_pub, args=(new_loop,message, topic))
            t.start()
            t.join()
            IOT.save()
            user.save()
        return redirect('/')
    except Exception as err:
        logger.error(err)
        return redirect('/')

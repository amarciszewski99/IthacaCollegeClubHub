from datetime import datetime
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegisterForm, AddClubForm, AddEventForm, JoinClubForm, JoinEventForm
from app.models import Member, Club, Event, MemberToClub, MemberToEvent


@app.route('/')
@app.route('/home')
@login_required
def home():
    member = Member.query.filter_by(email=current_user.email).first()
    return render_template('home.html', member=member)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        member = Member.query.filter_by(email=form.email.data).first()
        if member is None or not member.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for('login'))
        login_user(member, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)
    return render_template('login.html', title="Sign In", form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegisterForm()
    if form.validate_on_submit():
        member = Member(name=form.name.data, email=form.email.data, major=form.major.data, year=form.year.data)
        member.set_password(form.password.data)
        db.session.add(member)
        db.session.commit()
        flash('Registration successful, thank you!')
        return redirect(url_for('login'))
    return render_template('register.html', title="Register", form=form)


@app.route('/clubs')
def clubs():
    club_list = db.session.query(Club).all()
    return render_template('clubs.html', title="Clubs", club_list=club_list)


@app.route('/club/<name>', methods=['GET', 'POST'])
@login_required
def club(name):
    form = JoinClubForm()

    currentClub = Club.query.filter_by(name=name).first()
    isMember = MemberToClub.query.filter_by(memberID=current_user.id, clubID=currentClub.id).first()

    if form.validate_on_submit():
        if isMember is None:
            clubMember = MemberToClub(memberID=current_user.id, clubID=currentClub.id)
            db.session.add(clubMember)
            db.session.commit()
            return redirect(url_for('home'))
        else:
            flash("You are already a registered member of this club!")
            return render_template('club.html', title=currentClub.name, club=currentClub, form=form)

    return render_template('club.html', title=currentClub.name, club=currentClub, form=form)


@app.route('/event/<name>', methods=['GET', 'POST'])
@login_required
def event(name):
    form = JoinEventForm()
    event = Event.query.filter_by(name=name).first()
    return render_template('event.html', title=event.name, event=event, form=form)


@app.route('/my_events')
@login_required
def my_events():
    #WHY DOES THIS WORK??? HOW DOES IT KNOW WHICH MEMBER'S CLUBS TO QUERY FROM???
    events = Event.query.join(MemberToEvent).join(Member).all()
    return render_template('myEvents.html', events=events)


@app.route('/add_club', methods=['GET', 'POST'])
def add_club_form():
    form = AddClubForm()
    clubList = db.session.query(Club).all()
    for thisClub in clubList:
        if thisClub.name == form.name.data:
            flash("This club already exists.")
            return redirect(url_for('add_club'))
    if form.validate_on_submit():
        club = Club(name=form.name.data, description=form.description.data)
        db.session.add(club)
        db.session.commit()
        flash('New club added: {}'.format(form.name.data))
        return render_template('home.html')
    return render_template('addClub.html', form=form)


@app.route('/add_event', methods=['GET', 'POST'])
def add_event_form():
    form = AddEventForm()
    eventList = db.session.query(Event).all()
    for thisEvent in eventList:
        if (thisEvent.name == form.name.data) and (thisEvent.dateTime == form.date_time.data):
            flash("This event already exists")
            return redirect(url_for('add_event_form'))
    if form.validate_on_submit():
        event = Event(name=form.name.data, dateTime=form.date_time.data)
        db.session.add(event)
        db.session.commit()
        flash('New event added: {}'.format(form.name.data))
        return render_template('myEvents.html')
    return render_template('addEvent.html', form=form)


@app.route('/resetDB')
def resetDB():
    flash("Resetting database: deleting old data and repopulating with dummy data")
    # clear all data from all tables
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        print('Clear table {}'.format(table))
        db.session.execute(table.delete())
    db.session.commit()

    #Create Member objects
    member1 = Member(id=1, name="Member A", email="MemberA@mail.com", major="Computer Science", year=2021)
    db.session.add(member1)
    member2 = Member(id=2, name="Member B", email="MemberB@mail.com", major="Emerging Media", year=2022)
    db.session.add(member2)
    member3 = Member(id=3, name="Member C", email="MemberC@mail.com", major="Business", year=2023)
    db.session.add(member3)
    member4 = Member(id=4, name="Member D", email="MemberD@mail.com", major="Physical Therapy", year=2024)
    db.session.add(member4)
    member5 = Member(id=5, name="Member E", email="MemberE@mail.com", major="Music Education", year=2025)
    db.session.add(member5)
    member6 = Member(id=6, name="Member F", email="MemberF@mail.com", major="Pyrotechnics", year=2030)
    db.session.add(member6)
    admin = Member(id=7, name="Admin", email="admin@admin.com", major="Admin", year=2020)
    admin.set_password("1234")
    db.session.add(admin)

    #Create Club objects
    club1 = Club(id=1, name="Club A", description="Club A Description")
    db.session.add(club1)
    club2 = Club(id=2, name="Club B", description="Club B Description")
    db.session.add(club2)

    #Create Event objects
    event1 = Event(id=1, name="Event A", dateTime="%2021-%01-%01 %12:%00:%00", address="123 Main St", \
                   description="Event A Description", clubID=1)
    db.session.add(event1)
    event2 = Event(id=2, name="Event B", dateTime="%2021-%02-%02 %13:%00:%00", address="456 Love Lane", \
                   description="Event B Description", clubID=2)
    db.session.add(event2)
    event3 = Event(id=3, name="Event C", dateTime="2021-03-03 14:00:00", address="9 Pheasant Run, Holmdel, NJ, 07733",\
                   description="Event C Description", clubID=2)
    db.session.add(event3)

    #Assign MemberToClub
    MtC1 = MemberToClub(id=1, memberID=1, clubID=1, is_admin=True)
    db.session.add(MtC1)
    MtC2 = MemberToClub(id=2, memberID=2, clubID=1, is_admin=False)
    db.session.add(MtC2)
    MtC3 = MemberToClub(id=3, memberID=3, clubID=1, is_admin=False)
    db.session.add(MtC3)
    MtC4 = MemberToClub(id=4, memberID=4, clubID=2, is_admin=True)
    db.session.add(MtC4)
    MtC5 = MemberToClub(id=5, memberID=5, clubID=2, is_admin=False)
    db.session.add(MtC5)
    MtC6 = MemberToClub(id=6, memberID=6, clubID=2, is_admin=False)
    db.session.add(MtC6)
    adminToClub1 = MemberToClub(id=7, memberID=7, clubID=1, is_admin=True)
    db.session.add(adminToClub1)
    adminToClub2 = MemberToClub(id=8, memberID=7, clubID=2, is_admin=False)
    db.session.add(adminToClub2)


    #Assign MemberToEvent
    MtE1= MemberToEvent(id=1, memberID=1, eventID=1)
    db.session.add(MtE1)
    MtE2= MemberToEvent(id=2, memberID=2, eventID=1)
    db.session.add(MtE2)
    MtE3= MemberToEvent(id=3, memberID=3, eventID=1)
    db.session.add(MtE3)
    MtE4= MemberToEvent(id=4, memberID=4, eventID=2)
    db.session.add(MtE4)
    MtE5= MemberToEvent(id=5, memberID=5, eventID=2)
    db.session.add(MtE5)
    MtE6= MemberToEvent(id=6, memberID=6, eventID=2)
    db.session.add(MtE6)
    adminToEvent1 = MemberToEvent(id=7, memberID=7, eventID=1)
    db.session.add(adminToEvent1)
    admintToEvent2 = MemberToEvent(id=8, memberID=7, eventID=2)
    db.session.add(admintToEvent2)
    admintToEvent3 = MemberToEvent(id=9, memberID=7, eventID=3)
    db.session.add(admintToEvent3)

    db.session.commit()

    return render_template('resetDB.html')

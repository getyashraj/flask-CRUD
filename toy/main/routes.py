from flask_login import login_user, current_user, logout_user, login_required
from toy.main.forms import UpdateVaccineUnits, LoginForm, Request
from toy.main.forms import CenterAddition, VaccineAddition, UpdateCenterDetails
from toy.models import LoginDetails, Requests, User, Vaccines
from toy import db, bcrypt
from flask import (render_template, url_for, flash,
                   redirect, request, Blueprint)

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def home():
    return render_template('home.html')


@main.route('/addcenter', methods=['GET', 'POST'])
@login_required
def add_center():
    if (LoginDetails.query.filter_by(id=current_user.id).first()).is_admin:
        form = CenterAddition()
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(
                form.password.data).decode('utf-8')
            credentials = LoginDetails(
                password=hashed_password, is_admin=False)
            user = User(centername=form.centername.data, city=form.city.data,
                        state=form.state.data, pincode=form.pincode.data,
                        email=form.email.data)
            db.session.add(credentials)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('main.admin'))

        return render_template('add-center.html', title='add center',
                               form=form, admin=1)

    else:
        flash('Not an admin', 'danger')
        return render_template('access-denied.html')


@main.route('/addvaccine', methods=['GET', 'POST'])
@login_required
def add_vaccine():
    if (LoginDetails.query.filter_by(id=current_user.id).first()).is_admin:
        form = VaccineAddition()
        if form.validate_on_submit():
            vaccine = Vaccines(vaccinename=form.vaccinename.data,
                               manufacturing_company=form.manufacturing_company
                               .data,
                               quantity=form.quantity.data)
            db.session.add(vaccine)
            db.session.commit()
            return redirect(url_for('main.admin'))
        return render_template('add-vaccine.html', title='add vaccine',
                               form=form, admin=1)

    else:
        flash('Not an admin', 'danger')
        return render_template('access-denied.html')


@main.route('/updatecenter/<int:centerid>', methods=['GET', 'POST'])
@login_required
def update_center(centerid):
    if (LoginDetails.query.filter_by(id=current_user.id).first()).is_admin:
        center = User.query.get_or_404(centerid)
        form = UpdateCenterDetails()
        if form.validate_on_submit():
            center.centername = form.centername.data
            center.city = form.city.data
            center.state = form.state.data
            center.pincode = form.pincode.data
            center.email = form.email.data
            db.session.commit()
            return redirect(url_for('main.admin'))
        form.centername.data = center.centername
        form.city.data = center.city
        form.state.data = center.state
        form.pincode.data = center.pincode
        form.email.data = center.email
        return render_template('update-center.html', title='update center',
                               center=center, form=form, admin=1)
    else:
        flash('Not an admin', 'danger')
        return render_template('access-denied.html')


@main.route('/deletecenter/<int:centerid>', methods=['POST'])
@login_required
def delete_center(centerid):
    if (LoginDetails.query.filter_by(id=current_user.id).first()).is_admin:
        center = User.query.get_or_404(centerid)
        db.session.delete(center)
        db.session.commit()
        flash('Center Deleted', 'info')
        return redirect(url_for('main.display_centers'))

    else:
        flash('Not an admin', 'danger')
        return render_template('access-denied.html')


@main.route('/updatevaccine')
def update_vaccine():
    form = UpdateVaccineUnits()
    return render_template('update-vaccine.html', title='update vaccine',
                           form=form)


@main.route('/login', methods=['GET', 'POST'])
def login():
    if User.query.first():
        form = LoginForm()
        if form.validate_on_submit():
            if User.query.filter_by(email=form.email.data).first():
                user = User.query.filter_by(email=form.email.data).first()
                pass_data = LoginDetails.query.filter_by(id=user.id).first()
                if user and bcrypt.check_password_hash(pass_data.password,
                                                       form.password.data):
                    login_user(user, remember=form.remember.data)
                    flash('login successful', 'success')
                    next_page = request.args.get('next')
                    if next_page:
                        return redirect(next_page)

                    elif (LoginDetails.query.filter_by(id=current_user.id).
                            first()).is_admin:

                        return redirect(url_for('main.admin'))

                    else:
                        return redirect(url_for('main.user'))

                else:
                    flash('Login Unsuccessful', 'danger')
            else:
                flash('No user found with this email id', 'danger')
                return redirect(url_for('main.home'))

        return render_template('login.html', title='login', form=form)

    else:
        form = CenterAddition()
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(
                form.password.data).decode('utf-8')
            credentials = LoginDetails(
                password=hashed_password, is_admin=True)
            user = User(centername=form.centername.data, city=form.city.data,
                        state=form.state.data, pincode=form.pincode.data,
                        email=form.email.data)
            db.session.add(credentials)
            db.session.add(user)
            db.session.commit()
            flash('Admin created successfully', 'success')
            return redirect(url_for('main.admin'))
        flash('Create an admin user', 'info')
        return render_template('add-center.html', form=form)


@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@main.route('/admin')
@login_required
def admin():
    if (LoginDetails.query.filter_by(id=current_user.id).first()).is_admin:
        admin = 1
        center_count = User.query.join(
            LoginDetails, User.id == LoginDetails.id).\
            filter(LoginDetails.is_admin is False).count()
        vaccine_count = Vaccines.query.count()
        request_count = Requests.query.filter_by(status='Pending').count()
        return render_template('admin.html',
                               admin=admin, center_count=center_count,
                               vaccine_count=vaccine_count,
                               request_count=request_count)

    else:
        flash('NOT AN ADMIN', 'danger')
        return render_template('access-denied.html')


@main.route('/user')
@login_required
def user():
    if ((LoginDetails.query.filter_by(id=current_user.id).first()).is_admin
            is False):
        requests = Requests.query.filter_by(
            centerid=current_user.id)
        vaccine = Vaccines()
        return render_template('user.html', requests=requests,
                               vaccine=vaccine, user=1)
    else:
        flash('Only for Registered user', 'info')
        return render_template('access-denied.html')


@main.route('/centers')
@login_required
def display_centers():
    if (LoginDetails.query.filter_by(id=current_user.id).first()).is_admin:
        centers = User.query.join(
            LoginDetails, User.id == LoginDetails.id).\
            filter(LoginDetails.is_admin is False)
        return render_template('centers.html', centers=centers, admin=1)

    else:
        flash('NOT AN ADMIN', 'danger')
        return render_template('access-denied.html')


@main.route('/registeredcenters')
def centers():
    centers = User.query.join(
        LoginDetails, User.id == LoginDetails.id).\
        filter(LoginDetails.is_admin is False)
    return render_template('registered-centers.html', centers=centers)


@main.route('/registeredvaccines')
def vaccines():
    vaccines = Vaccines.query.all()
    return render_template('registered-vaccines.html', vaccines=vaccines)


@main.route('/vaccinerequest', methods=['GET', 'POST'])
@login_required
def vaccine_request():
    if ((LoginDetails.query.filter_by(id=current_user.id).first()).is_admin
            is False):
        form = Request()
        vaccineid = Vaccines.query.filter_by(
            vaccinename=form.vaccinename.data).first()
        if form.validate_on_submit():
            request = Requests(centerid=current_user.id,
                               vaccineid=vaccineid.id,
                               quantity=form.quantity.data, status='Pending')
            db.session.add(request)
            db.session.commit()
            flash('Request Successfully Sent', 'success')
            return redirect(url_for('main.user'))

        return render_template('requests.html', form=form, user=1)
    else:
        flash('Only For Registered Centers', 'info')
        return redirect(url_for('main.home'))


@main.route('/updaterequest', methods=['GET', 'POST'])
@login_required
def update_request():
    if (LoginDetails.query.filter_by(id=current_user.id).first()).is_admin:
        requests = Requests.query.filter_by(status="Pending")
        center = User()
        vaccine = Vaccines()

        return render_template('update-request.html', requests=requests,
                               center=center, vaccine=vaccine, admin=1)
    else:
        flash('NOT AN ADMIN', 'danger')
        return render_template('access-denied.html')


@main.route('/rejectrequest/<int:requestid>', methods=['POST'])
@login_required
def reject_request(requestid):
    if (LoginDetails.query.filter_by(id=current_user.id).first()).is_admin:
        request = Requests.query.get_or_404(requestid)
        request.status = 'REJECTED'
        db.session.commit()
        flash('Request rejected', 'info')
        return redirect(url_for('main.update_request'))

    else:
        flash('Not an admin', 'danger')
        return render_template('access-denied.html')


@main.route('/approverequest/<int:requestid>', methods=['POST'])
@login_required
def approve_request(requestid):
    if (LoginDetails.query.filter_by(id=current_user.id).first()).is_admin:
        request = Requests.query.get_or_404(requestid)
        request.status = 'APPROVED'
        db.session.commit()
        flash('Request approved', 'info')
        return redirect(url_for('main.update_request'))

    else:
        flash('Not an admin', 'danger')
        return render_template('access-denied.html')

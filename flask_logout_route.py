from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, logout_user
from . import main
from .forms import LogoutConfirmationForm

@main.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    form = LogoutConfirmationForm()
    if form.validate_on_submit():
        logout_user()
        flash('You have been logged out successfully.', 'success')
        return redirect(url_for('main.login'))
    return render_template('logout.html', form=form)

# Add this to your forms.py
from flask_wtf import FlaskForm

class LogoutConfirmationForm(FlaskForm):
    pass  # We only need CSRF protection, no fields required

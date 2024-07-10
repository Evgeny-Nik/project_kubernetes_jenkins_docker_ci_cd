"""Module for running a flask python app using visual crossing api."""
from flask import Flask, render_template, request  # for flask methods
from weather_funcs import send_request
import custom_exceptions


app = Flask(__name__)


HOMEPAGE = "index.html"
ERROR_PAGE = "error.html"


@app.route('/', methods=['GET', 'POST'])
def render_page():
    """function used to hangle user's get and post requests
       on get it loads the basic website ui
       on post it loads data for the requested city"""
    # use get http method connect to target_API
    if request.method == 'POST':
        try:
            city_name = request.form['city_name']
            weather_data_list = send_request(city_name)
            return render_template(HOMEPAGE, data_list=weather_data_list)
        except custom_exceptions.DataError as err_msg:
            return render_template(HOMEPAGE, error=err_msg, city_name=city_name)
    return render_template(HOMEPAGE)


@app.errorhandler(404)
def render_error():
    """error handler, loads error page if something goes wrong"""
    return render_template(ERROR_PAGE)


if __name__ == '__main__':
    # run with possible remote access
    app.run()

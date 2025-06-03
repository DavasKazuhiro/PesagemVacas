from flask import Blueprint, request, render_template, redirect, url_for

mqtt_ = Blueprint("mqtt_", __name__ , template_folder="views")
from celery import shared_task
from apktool_decompiler import decompile
from smali_analizer import  smali_method_extracter

@shared_task
def analize_apk(path):
    decompile.decompile(path)
    smali_method_extracter
    print(path)
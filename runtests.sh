#!/bin/bash

py.test -s --pyargs speedcom --cov-report term-missing --cov=speedcom --cov-config .coveragerc
rm speedcom/tests/__pycache__/*

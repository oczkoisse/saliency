%module bmsl

%include <opencv.i>
%cv_instantiate_all_defaults

%{
#include "BMS.h"
#include <vector>
#include <cmath>
#include <ctime>
%}

%include "BMS.h"

#include "cvgabor.h"

#include <iostream>

int main(int argc, char** argv)
{
	double Sigma = PI;
	double F = sqrt(2.0);
	CvGabor *gabor1 = new CvGabor;
	gabor1->Init(PI, 3, Sigma, F);
	
	IplImage *kernel = cvCreateImage( cvSize(gabor1->get_mask_width(), gabor1->get_mask_width()), IPL_DEPTH_8U, 1);
	kernel = gabor1->get_image(CV_GABOR_REAL);
	cvNamedWindow("Gabor Kernel", 1);
	cvShowImage("Gabor Kernel", kernel);
	cvWaitKey(0);
	cvDestroyWindow("Gabor Kernel");
	cvReleaseImage(&kernel);
	
	IplImage *img = cvLoadImage( "/Users/oliver/Projects/Personal/CV/ANPR/Data/Resized/DSCF4798.JPG", CV_LOAD_IMAGE_GRAYSCALE );
	cvNamedWindow("Original Image", 1);
	cvShowImage("Original Image", img);
	cvWaitKey(0);
	cvDestroyWindow("Original Image");
	
	IplImage *real = cvCreateImage(cvSize(img->width,img->height), IPL_DEPTH_8U, 1);
	gabor1->conv_img(img, real, CV_GABOR_REAL);
	cvNamedWindow("Real Response", 1);
	cvShowImage("Real Response",real);
	cvWaitKey(0);
	cvDestroyWindow("Real Response");
	
	IplImage *imag = cvCreateImage(cvSize(img->width,img->height), IPL_DEPTH_8U, 1);
	gabor1->conv_img(img, imag, CV_GABOR_IMAG);
	cvNamedWindow("Imaginary Response", 1);
	cvShowImage("Imaginary Response",imag);
	cvWaitKey(0);
	cvDestroyWindow("Imaginary Response");
	
	IplImage *mag = cvCreateImage(cvSize(img->width,img->height), IPL_DEPTH_8U, 1);
	gabor1->conv_img(img, mag, CV_GABOR_MAG);
	cvNamedWindow("Magnitude Response", 1);
	cvShowImage("Magnitude Response",mag);
	cvWaitKey(0);
	cvDestroyWindow("Magnitude Response");
	
	delete gabor1;
}
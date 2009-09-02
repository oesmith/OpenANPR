#include "cvgabor.h"

#include <iostream>

void conv(IplImage* src, IplImage* dst, double phi, double nu)
{
	double Sigma = PI/2;
	CvGabor* gabor = new CvGabor(phi, nu);
	
	gabor->conv_img(src, dst, CV_GABOR_PHASE);
	
	delete gabor;
}

int main(int argc, char** argv)
{
	IplImage *img = cvLoadImage( "/Users/oliver/Projects/Personal/CV/ANPR/Data/Resized/mazdas_small.jpg");
	cvNamedWindow("Original Image", 1);
	cvShowImage("Original Image", img);
	cvWaitKey(0);
	cvDestroyWindow("Original Image");
	
	IplImage* foo = cvCreateImage(cvSize(img->width, img->height), IPL_DEPTH_8U, 3);
	cvPyrMeanShiftFiltering(img, foo, 20, 20, 3);
	cvNamedWindow("Colour", 1);
	cvShowImage("Colour",foo);
	cvWaitKey(0);
	cvDestroyWindow("Colour");
	
	IplImage* bar = cvCreateImage(cvSize(img->width, img->height), IPL_DEPTH_8U, 1);
	cvCvtColor(foo,bar,CV_BGR2GRAY);
	cvEqualizeHist(bar,bar);
	cvNamedWindow("Grey", 1);
	cvShowImage("Grey",bar);
	cvWaitKey(0);
	cvDestroyWindow("Grey");
	
	cvSmooth(bar,bar);
	
	IplImage* acc = cvCreateImage(cvSize(img->width, img->height), IPL_DEPTH_32F, 1);
	
	for(int j=0;j<2;j++)
	{
		double freq = sqrt(2.0) / (4*(j+1));
		for(int i=0;i<4;i++)
		{
			IplImage *mag = cvCreateImage(cvSize(img->width,img->height), IPL_DEPTH_8U, 1);
			conv(bar, mag, i*PI/4.0, freq);
			cvAcc(mag,acc);
			cvReleaseImage(&mag);
		}
	}
	
	IplImage* final = cvCreateImage(cvSize(img->width, img->height), IPL_DEPTH_8U, 1);
	cvConvertScale(acc,final,0.04,0.0);
	cvNamedWindow("Final", 1);
	cvShowImage("Final",final);
	cvWaitKey(0);
	cvDestroyWindow("Final");
	
}
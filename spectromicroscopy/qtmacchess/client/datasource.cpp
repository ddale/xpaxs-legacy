#include <qfile.h>
#include <qstring.h>
#include <qtextstream.h>
#include "datasource.h"

/* IMPORTANT: must declare static variables here to avoid "undefined reference" errors on compile */

/* Connection Related */
bool DataSource :: connectToMotor;
bool DataSource :: connectToZoomFocus;
bool DataSource :: connectedToMotor;
bool DataSource :: connectedToZoomFocus;
bool DataSource :: connectedToVideo;
bool DataSource :: directCompumotor;
int DataSource :: videoPort;    
int DataSource :: cmotorPort;
int DataSource :: zfmotorPort;
QString DataSource :: videoIP;
QString DataSource :: cmotorIP;
QString DataSource :: zfmotorIP;
 
 
 /* Compumotor Related */
bool DataSource :: motor_busy;
 
float DataSource :: pinStep; 
float DataSource :: cor45;
float DataSource :: cor135;
float DataSource :: corZ;

/* Zoom / Focus */
bool DataSource :: enableFocus;
int DataSource :: zoomLimit;
int DataSource :: focusLimit;
int DataSource :: zoomCurrent;
float DataSource :: pixPerMicron;
int DataSource :: focusCurrent;
float DataSource :: zoomSlope;
float DataSource :: zoomIntercept;

/* Video Streaming */
int DataSource :: quality;
int DataSource :: bitrate;
int DataSource :: resolution;

/* Midpoint Tool Related */
bool DataSource :: midpointToolEnabled;
int DataSource :: upperLineY;
int DataSource :: lowerLineY;
int DataSource :: centerY;
int DataSource :: centerX;
int DataSource :: midLineY;
int DataSource :: vertLineX;
bool DataSource :: newMidpoint;
bool DataSource :: midpointTool;

/* Crosshair / Beam Diameter Display Related */
float DataSource :: crossX; 
float DataSource :: crossY;
int DataSource::zcenX;
int DataSource::zcenY;

bool DataSource :: crossHairEnabled;
bool DataSource :: crossHairDisplayed;
bool DataSource :: newCrossHair;
int DataSource :: beam_dia;

/* Scale Display Related */
bool DataSource :: barDisplayed;
float DataSource :: zoomFactor; 

bool DataSource :: clickAndMove;


void DataSource :: initialize()
{
    /* Open the File */
    QFile settings(QString("test.conf"));
    QString s = "";
    settings.open(IO_ReadOnly);
    
    while(settings.readLine(s,50) > 0)
    {
 	if(s == "connectToMotor\n")
	{
	    settings.readLine(s, 50);
	    connectToMotor = s.toInt() ? true : false;
	    fprintf(stderr,"found 1\n");	    
	}
	else if(s == "connectToZoomFocus\n")
	{   
	    settings.readLine(s, 50);
	    connectToZoomFocus = s.toInt() ? true : false;
	    	    fprintf(stderr,"found 2\n");	 
	}
	else if(s == "directCompumotor\n")
	{    
	    settings.readLine(s, 50);
	    directCompumotor = s.toInt() ? true : false;
	    	    fprintf(stderr,"found 3\n");	 
	}
	else if(s == "videoPort\n")
	{    
	    settings.readLine(s, 50);
	    videoPort = s.toInt();
	    	    fprintf(stderr,"found 4\n");	     
	}
	else if(s == "cmotorPort\n")
	{	    
	    settings.readLine(s, 50);
	    cmotorPort = s.toInt();
	} 
	else if(s == "zfmotorPort\n")
	{    
	    settings.readLine(s, 50);
	    zfmotorPort = s.toInt();
	}
	else if(s == "videoIP\n")
	{	    
	    settings.readLine(s, 50);    
	    videoIP = s;
	}
	else if(s == "cmotorIP\n")
	{	    
	    settings.readLine(s, 50);    
	    cmotorIP = s;
	}
	else if(s == "zfmotorIP\n")
	{	    
	    settings.readLine(s, 50);    
	    zfmotorIP = s;
	}
	else if(s == "enableFocus\n")
	{    
	    settings.readLine(s, 50);
	    enableFocus = s.toInt() ? true : false;
	}
	else if(s == "quality\n")
	{    
	    settings.readLine(s, 50);
	    quality = s.toInt();
	}
	else if(s == "bitrate\n")
	{    
	    settings.readLine(s, 50);    
	    bitrate = s.toInt();
	}
	else if(s == "resolution\n")
	{	    
	    settings.readLine(s, 50);    
	    resolution = s.toInt();	
	}
    	else if(s == "crossX\n")
	{
	    settings.readLine(s, 50);    
	    crossX = s.toFloat(); 
	}
	else if(s == "crossY\n")
	{	    
	    settings.readLine(s, 50);    
	    crossY = s.toFloat();	
	}
	else if(s == "crossHairDisplayed\n")
	{	    
	    settings.readLine(s, 50);
	    crossHairDisplayed = s.toInt() ? true : false;
	}
	else if(s == "beam_dia\n")
	{   
	    settings.readLine(s, 50);	
	    beam_dia = s.toInt();
	}
	else if(s == "barDisplayed\n")
	{    
	    settings.readLine(s, 50);
	    barDisplayed = s.toInt() ? true : false;
	}
	else if(s == "upperLineY\n")
	{	    
	    settings.readLine(s, 50);    
	    upperLineY = s.toInt();	
	}
	else if(s == "lowerLineY\n")
	{	    
	    settings.readLine(s, 50);    
	    lowerLineY = s.toInt();	
	}
	else if(s == "centerY\n")
	{	    
	    settings.readLine(s, 50);    
	    centerY = s.toInt();	
	}			
	else if(s == "centerX\n")
	{	    
	    settings.readLine(s, 50);    
	    centerX = s.toInt();	
	}
	else if(s == "midLineY\n")
	{	    
	    settings.readLine(s, 50);    
	    midLineY = s.toInt();	
	}
	else if(s == "vertLineX\n")
	{	    
	    settings.readLine(s, 50);    
	    vertLineX = s.toInt();	
	}	
	else if (s == "pinStep\n")
	{
	    settings.readLine(s,50);
	    pinStep = s.toFloat();
	}
	else if (s == "zcenX\n")
	{
	    settings.readLine(s,50);
	    zcenX = s.toInt();
	}	
	else if (s == "zcenY\n")
	{
	    settings.readLine(s,50);
	    zcenY = s.toInt();
	}	
	else if (s == "cor45\n")
	{
	    settings.readLine(s,50);
	    cor45 = s.toFloat();
	}	
	else if (s == "cor135\n")
	{
	    settings.readLine(s,50);
	    cor135 = s.toFloat();
	}	
	else if (s == "corZ\n")
	{
	    settings.readLine(s,50);
	    corZ = s.toFloat();
	}
	else if (s == "zoomSlope\n")
	{
	    settings.readLine(s,50);
	    zoomSlope = s.toFloat();
	}
	else if (s == "zoomIntercept\n")
	{
	    settings.readLine(s,50);
	    zoomIntercept = s.toFloat();
	}
    }
    
     connectedToMotor = false;
    connectedToZoomFocus = false;
    connectedToVideo = false;
    motor_busy = true;
    zoomLimit = focusLimit = zoomCurrent = focusCurrent = -1;
    midpointToolEnabled = false;
    crossHairEnabled = false;
    midpointTool = false;
    clickAndMove = false;
    
  // actual zoom center on image in pixels (obtained experimentally)
  // This is the point which does not move when you zoom the image. 
  // It is measured in pixel coordinates on the fully zoomed out image.
  // If you don't get this point right, the crosshairs will not move to the 
  // correct location when you zoom.
    
  //  zcenX = 402;
  //  zcenY = 376;
  
// F1 scope    
//    zcenX = 387;
//   zcenY = 373;
    
 // F2 scope
 //   zcenX = 592;
 //   zcenY = 328;
    
    // experimenally determined scale factors for 
    // pin motion (unitless) converts desired distance
    // to distance value needed to accomplish that 
    // amount of movement. Should be 1.0, but can be
    // used to correct motor directions and gear ratios.
    
    
   // These are values for  current F1 system
    //  cor45 = 10.0;
    // cor135 = -10.0;
    // corZ = 2.3;
    
    // These are values for current F2 system
    
//   cor45 = 0.4;
 //  cor135 = 0.4;
 //  corZ = 0.7;
        
 /* These are local.
    upperLineY;
    lowerLineY;
    centerY;
    centerX;
    midLineY;
    */

    settings.close();
}


void DataSource ::save()
{
        /* Open the File */
    QFile settings(QString("test.conf"));
    QString s = "";
    settings.open(IO_WriteOnly | IO_Truncate );
    QTextStream a(&settings);
   
    a << "connectToMotor\n";
    a << (connectToMotor ? "1\n" : "0\n");
    
    a << "connectToZoomFocus\n";
    a << (connectToZoomFocus ? "1\n" : "0\n");
    
    a << "directCompumotor\n";
    a << (directCompumotor ? "1\n" : "0\n");
    
    a << "videoPort\n";
    a << videoPort << "\n";    
    
    a << "cmotorPort\n";
    a << cmotorPort << "\n";
    
    a << "zfmotorPort\n";
    a << zfmotorPort << "\n";
    
    a << "videoIP\n";
    a << videoIP;
    
    a << "cmotorIP\n";
    a << cmotorIP;
    
    a << "zfmotorIP\n";
    a << zfmotorIP;
    
    a << "enableFocus\n";
    a << (enableFocus ? "1\n" : "0\n");
    

    a << "quality\n";
    a << quality << "\n";
    
    a << "bitrate\n";
    a << bitrate << "\n";
    
    a << "resolution\n";
    a << resolution << "\n";
    
    a << "crossX\n";
    a << crossX << "\n";
    
    a << "crossY\n";
    a << crossY << "\n";
    
    a << "crossHairDisplayed\n";
    a << (crossHairDisplayed ? "1\n" : "0\n");
    
    a << "beam_dia\n";
    a << beam_dia << "\n";
    
    a << "barDisplayed\n";
    a << (barDisplayed ? "1\n" : "0\n");
    
    a << "upperLineY\n";
    a << upperLineY << "\n";
    
    a << "lowerLineY\n";
    a << lowerLineY << "\n";
    
    a << "centerY\n";
    a << centerY << "\n";
    
    a << "centerX\n";
    a << centerX << "\n";    
    
    a << "midLineY\n";
    a << midLineY << "\n";   	        
    
    a << "vertLineX\n";
    a << vertLineX << "\n";   	        
    
    a << "pinStep\n";
    a << pinStep << "\n";
    
    a << "zcenX\n";
    a << zcenX << "\n";
    
     a << "zcenY\n";
    a << zcenY << "\n";
    
    a << "cor45\n";
    a << cor45 << "\n";
    
    a << "cor135\n";
    a << cor135 << "\n";
       
    a << "corZ\n";
    a << corZ << "\n";
    
    a << "zoomSlope\n";
    a << zoomSlope << "\n";
    
    a << "zoomIntercept\n";
    a << zoomIntercept << "\n";
        
    settings.close();     
}


void DataSource ::saveDefaults()
{
        /* Open the File */
    QFile settings(QString("test.conf"));
    QString s = "";
    settings.open(IO_WriteOnly | IO_Truncate );
    QTextStream a(&settings);
    
    a << "connectToMotor\n";
    a << "1\n";
    
    a << "connectToZoomFocus\n";
    a << "1\n";
    
    a << "directCompumotor\n";
    a << "0\n";
    
    a << "videoPort\n";
    a << 1394 << "\n";    
    
    a << "cmotorPort\n";
    a << 5002 << "\n";
    
    a << "zfmotorPort\n";
    a << 4001 << "\n";
    
    a << "videoIP\n";
    a << "128.84.182.123\n";    
    
    a << "cmotorIP\n";
    a << "128.84.182.51\n";
    
    a << "zfmotorIP\n";
    a << "128.84.182.123\n";   
    
    a << "enableFocus\n";
    a << "1\n";
    
    a << "quality\n";
    a << 6 << "\n";
    
    a << "bitrate\n";
    a << 900 << "\n";
    
    a << "resolution\n";
    a << 1024 << "\n";
    
    a << "crossX\n";
    a << -1.0 << "\n";
    
    a << "crossY\n";
    a << -1.0 << "\n";
    
    a << "crossHairDisplayed\n";
    a << "1\n";
    
    a << "beam_dia\n";
    a << 50 << "\n";
    
    a << "barDisplayed\n";
    a << "1\n";
    
    a << "upperLineY\n";
    a << 0 << "\n";
    
    a << "lowerLineY\n";
    a << 500 << "\n";
    
    a << "centerY\n";
    a << -1 << "\n";
    
    a << "centerX\n";
    a << -1 << "\n";    
    
    a << "midLineY\n";
    a << 250 << "\n";  
    
    a << "vertLineX\n";
    a << 512 << "\n";  
    
    a << "pinStep\n";
    a << 0.544 << "\n";
    
    a << "zoomSlope\n";
    a << 9.06908e-05 << "\n";
    
    a << "zoomIntercept\n";
    a << -1.29565 << "\n";
    
     settings.close();
}




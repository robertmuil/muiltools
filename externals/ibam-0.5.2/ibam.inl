// IBAM, the Intelligent Battery Monitor
// Copyright (C) 2001-2003, Sebastian Ritterbusch (IBAM@Ritterbusch.de)
//
// This program is free software; you can redistribute it and/or
// modify it under the terms of the GNU General Public License
// as published by the Free Software Foundation; either version 2
// of the License, or (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program; if not, write to the Free Software
// Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
//

#include <iostream>
#include <sstream>
#include <fstream>
#include <string>
#include <math.h>
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <time.h>
#include <dirent.h> // for acpi multiple batteries

#ifndef NO_LOCALE_H 
   #include <locale.h> // thus I may prevent evil krells to change to others.. 
#endif

#ifndef NO_MKDIR
   #include <sys/stat.h>  // for mkdir
   #include <sys/types.h> // for mkdir
#endif

/* Arguments, with symbols from linux/apm_bios.h.  Information is
+          from the Get Power Status (0x0a) call unless otherwise noted.
+
+          0) Linux driver version (this will change if format changes)
+          1) APM BIOS Version.  Usually 1.0 or 1.1.
+          2) APM flags from APM Installation Check (0x00):
+             bit 0: APM_16_BIT_SUPPORT
+             bit 1: APM_32_BIT_SUPPORT
+             bit 2: APM_IDLE_SLOWS_CLOCK
+             bit 3: APM_BIOS_DISABLED
+             bit 4: APM_BIOS_DISENGAGED
+          3) AC line status
+             0x00: Off-line
+             0x01: On-line
+             0x02: On backup power (APM BIOS 1.1 only)
+             0xff: Unknown
+          4) Battery status
+             0x00: High
+             0x01: Low
+             0x02: Critical
+             0x03: Charging
+             0xff: Unknown
+          5) Battery flag
+             bit 0: High
+             bit 1: Low
+             bit 2: Critical
+             bit 3: Charging
+             bit 7: No system battery
+             0xff: Unknown
+          6) Remaining battery life (percentage of charge):
+             0-100: valid
+             -1: Unknown
+          7) Remaining battery life (time units):
+             Number of remaining minutes or seconds
+             -1: Unknown
+          8) min = minutes; sec = seconds */

inline int battery_status::onBattery(void) const { return acLineStatus==0; }
inline int battery_status::charging(void)  const { return chargeStatus; }
inline int battery_status::percent(void)   const { return remainingBatteryPercent; }
inline float battery_status::subpercent(void) const { return remainingBatterySubPercent; } 
inline int battery_status::seconds(void)   const { return remainingBatteryLifeSeconds; } 

inline battery_status::battery_status(string path) {
   Path = path;
   remainingBatterySubPercent=-1;
}

inline battery_status::~battery_status(void) { }

inline void battery_status::update(void) {
   cout << "battery_status::update() called. This should never happen!" << endl;
}


inline apm_status::apm_status(string path) : battery_status(path)
{
   update();
}

inline pmu_status::pmu_status(string path) : battery_status(path)
{
   update();
}

inline acpi_status::acpi_status(string path) : battery_status(path)
{
   update();
}

inline sysfs_status::sysfs_status(string path) : battery_status(path)
{
   update();
}

inline void apm_status::update(void)
{
   ifstream in;
   int i;  
   in.open(Path.c_str());
   for(i=0;i<10 && in.fail();i++)
      in.open(Path.c_str());
   if(in.fail())
   {
      acLineStatus=0;
      batteryStatus=0;
      chargeStatus=0;
      remainingBatteryPercent=-1;
      remainingBatteryLifeSeconds=-1;
      return; 
   }
   string driverVersion, biosVersion;
   int apmFlags, batteryFlag;
   char c,d;
   in >> driverVersion;
   in >> biosVersion;
   in >> c >> d; // 0x
   in >> c >> d; 
   apmFlags=(c>'9'?c-'a'+10:c-'0')*16+(d>'9'?d-'a'+10:d-'0');
   in >> c >> d; // 0x
   in >> c >> d; 
   acLineStatus=(c>'9'?c-'a'+10:c-'0')*16+(d>'9'?d-'a'+10:d-'0');
   in >> c >> d; // 0x
   in >> c >> d; 
   batteryStatus=(c>'9'?c-'a'+10:c-'0')*16+(d>'9'?d-'a'+10:d-'0');
   in >> c >> d; // 0x
   in >> c >> d; 
   batteryFlag=(c>'9'?c-'a'+10:c-'0')*16+(d>'9'?d-'a'+10:d-'0');
   chargeStatus = (batteryFlag&8)!=0;
   in >> remainingBatteryPercent >> c; // % 
   string minsec; 
   in >> remainingBatteryLifeSeconds >> minsec; 
   if(minsec=="min") remainingBatteryLifeSeconds*=60;
#ifdef IBAM_DEBUG
   cout << "Driver Version:    " << driverVersion << endl;
   cout << "Bios Version:      " << biosVersion << endl;
   cout << "APM Flags:         " << apmFlags << endl;
   cout << "AC Line Status:    " << acLineStatus << endl;
   cout << "Battery Status:    " << batteryStatus << endl;
   cout << "Battery Flag:      " << batteryFlag << endl;
   cout << "Remaining Percent: " << remainingBatteryPercent << endl;
   cout << "Remaining Seconds: " << remainingBatteryLifeSeconds << endl;
#endif
}

// PMU File-format
//
// 2 batteries, running on battery
//
// /proc/pmu/info:
//
// PMU driver version     : 2
// PMU firmware version   : 0c
// AC Power               : 0
// Battery count          : 2
//
// 1)  Note that there are systems where AC Power may falsely show 0 if the 
//     computer booted without any batteries plugged in. The battery-flags
//     are reported to be more reliable in that case.
//     This is *not* yet taken into account by ibam.
//
// 2)  The battery count only reflects the number of theoretically available
//     battery slots and not the number of batteries currently in the system.
//
// /proc/pmu/battery_0:
//
// flags      : 00000011
// charge     : 5788
// max_charge : 5789
// current    : 0
// voltage    : 12549
// time rem.  : 0
//
// /proc/pmu_battery_1:
//
// flags      : 00000011
// charge     : 518
// max_charge : 1112
// current    : -1087
// voltage    : 11324
// time rem.  : 1715
//
// case no battery:
//
// flags      : 00000010
// charge     : 0
// max_charge : 0
// current    : 0
// voltage    : 0
// time rem.  : 0
//
// 1)  flags is to be read hexadeicmal (or binary perhaps?), bit 0
//     denotes if this battery is present, bit 1 denotes reportingly
//     rather unreliable a charging state.
//
// 2)  A positive current denotes charging more reliably. (unchecked)
//     This is *not* yet taken into account, because it's unclear how this
//     reading behaves with two batteries.
//


inline void pmu_status::update(void)
{
   ifstream in;
   int i;
   in.open((Path+"/info").c_str());

   if (in.fail())
   {
      acLineStatus = 0;
      chargeStatus = 0;
      remainingBatteryLifeSeconds = -1;
      remainingBatteryPercent = -1;
      return;
   }

   stringbuf buf;
   char c;
   int d, cur_charge = 0, max_charge = 0;
   for (i = 0; i < 4; i++) {
      in.get(buf, ':');
      in >> c >> d;
      if (i == 2)
         acLineStatus = d;
   }
   in.close();
   in.open((Path+"/battery_0").c_str());

   if (in.fail()) {
      acLineStatus = 0;
      chargeStatus = 0;
      remainingBatteryLifeSeconds = -1;
      remainingBatteryPercent = -1;
      return;
   }

   for (i = 0; i < 6; i++) {
      in.get(buf, ':');
      in >> c >> d;
      if (i == 0)
         chargeStatus = (d&2)==0;
      if (i == 1)
         cur_charge = d;
      if (i == 2)
         max_charge = d;
      if (i == 5)
         remainingBatteryLifeSeconds = d;
   }

   in.close();
   in.open((Path+"/battery_1").c_str());

   if (in.fail()) {
      remainingBatteryPercent = (int)(cur_charge*100/max_charge);
      return;
   }

   for (i = 0; i < 6; i++) {
      in.get(buf, ':');
      in >> c >> d;
      if (i == 0)
         chargeStatus = (d&2)==0;
      if (i == 1)
         cur_charge += d;
      if (i == 2)
         max_charge += d;
      if (i == 5)
         remainingBatteryLifeSeconds += d;
   }

   remainingBatteryPercent = (int)(cur_charge*100/max_charge);
}

// Acpi Percentage and Remaining time computation based upon
// http://www.acpi.info/spec.htm V3.0
//
// [...]
// 3.9.3 Battery Gas Gauge
//
// At the most basic level, the OS calculates Remaining Battery 
// Percentage [%] using the following formula:
//
//                                    Battery Remaining Capacity [mAh/mWh]
// Remaining Battery Percentage [%] = ------------------------------------ * 100
//                                    Last Full Charged Capacity [mAh/mWh]
//
// Control Method Battery also reports the Present Drain Rate [mA or mW]
// for calculating the remaining battery life. At the most basic level,
// Remaining Battery life is calculated by following formula:
// 
//                              Battery Remaining Capacity [mAh/mWh]
// Remaining Battery Life [h] = ------------------------------------
//                              Battery Present Drain Rate [mA/mW]
//
// Smart Batteries also report the present rate of drain, but since they
// can directly report the estimated runtime, this function should be used
// instead as it can more accurately account for variations specific to
// the battery
// [...]
//
// I don't have a "Smart Battery", so I don't know, how /proc/acpi would
// report that. Contributions are greatly appreciated.
//
// See also http://www.tldp.org/HOWTO/ACPI-HOWTO/usingacpi.html
//

inline void acpi_status::update(void)
{
   ifstream in;
   DIR *acpi_battery_dir;
   struct dirent *battery_entry;
   int i;

   acpi_battery_dir=opendir((Path+"/battery").c_str());
   
   if (acpi_battery_dir==NULL) 
   {
      acLineStatus = 0;
      chargeStatus = 0;
      remainingBatteryLifeSeconds = -1;
      remainingBatteryPercent = -1;
      return;
   }

   long total_capacity=0;
   long total_remain=0;
   long total_rate=0;
    
   while ((battery_entry=readdir(acpi_battery_dir)))
   {
      if(battery_entry->d_name!=string(".") 
      && battery_entry->d_name!=string(".."))
      {
         in.open((((Path+"/battery/")+battery_entry->d_name)+"/info").c_str());
         stringbuf buf;
         char c;
         int capacity=0;
        
         for (i=0; i<3; i++) 
         {
            in.get(buf, ':');
            in >> c;
            if (i==0)
            {
               in >> c;
               if(c!='y') // present: yes
                  i=3;
            } else if(i==2)
            {
               in >> capacity;
               total_capacity+=capacity;
            }
         }
         
         in.close();

         #ifdef IBAM_DEBUG
            cout << "Battery "<<battery_entry->d_name<<":    Capacity " << capacity;
         #endif
         
         if(capacity)
         {
            in.open((((Path+"/battery/")+battery_entry->d_name)+"/state").c_str());

            for (i=0; i<5; i++) 
            {
               in.get(buf, ':');
               in >> c;
               if (i==2)
               {
                  char d,e,f,g,h;
                  in >> c >> d >> e >> f >> g >> h; // OUCH... #-} Somebody, please fix me
                  if(c=='c' && h=='i') // charging state: charging
                  {
                     acLineStatus=1;
                     batteryStatus=3;
                     chargeStatus=1;
                     #ifdef IBAM_DEBUG
                        cout << " charging";
                     #endif
                  } else
                  if(c=='d') // charging state: discharge
                  {
                     acLineStatus=0;
                     batteryStatus=0;
                     chargeStatus=0;
                     #ifdef IBAM_DEBUG
                        cout << " discharging";
                     #endif
                  } else
                  if(c=='c' && h=='e') // charging state: charged
                  {
                     acLineStatus=1;
                     batteryStatus=0;
                     chargeStatus=0;
                     #ifdef IBAM_DEBUG
                        cout << " charged";
                     #endif
                  }
               } else 
               if(i==3)
               {
                  int rate=0;
                  in >> rate;
                  total_rate+=rate;
                  #ifdef IBAM_DEBUG
                     cout << " Rate " << rate;
                  #endif

               } else
               if(i==4)
               {
                  int remain=0;
                  in >> remain;
                  total_remain+=remain;
                  #ifdef IBAM_DEBUG
                     cout << " Remain " << remain;
                  #endif
               } 
            }
            in.close();

         } // has capacity

         #ifdef IBAM_DEBUG
            cout << endl;
         #endif

      }
   }
   closedir(acpi_battery_dir);

   if(total_capacity)
   {
      remainingBatteryPercent=int((100.*total_remain)/total_capacity+.5);
      remainingBatterySubPercent=100.*total_remain/total_capacity+.5-remainingBatteryPercent;
   }
   else
   {
      remainingBatteryPercent=100;
      remainingBatterySubPercent=0;
   }
            
   if(remainingBatteryPercent>100)
   {
      remainingBatteryPercent=100; // Don't ask...
      remainingBatterySubPercent=0;
   }

   if(remainingBatteryPercent<100 && acLineStatus==1 && chargeStatus==0) // Deal with strange Acpi-Data?
   {
      //  either
      // acLineStatus=1;
      // batteryStatus=3;
      // chargeStatus=1;
      //  or
      // nothing (or is it just occuring because of late last_full_capacity update?)
      //  or
      // since it seems it starts at 100% for discharge
      remainingBatteryPercent=100;
      remainingBatterySubPercent=0;
   }

   if(total_rate)
   {
      if(chargeStatus)
      {
         remainingBatteryLifeSeconds=((total_capacity-total_remain)*60*60)/total_rate;
         if(remainingBatteryLifeSeconds<0)
            remainingBatteryLifeSeconds=0;
      }
      else
         remainingBatteryLifeSeconds=(total_remain*60*60)/total_rate;
   }
   else
      remainingBatteryLifeSeconds=(remainingBatteryPercent*IBAM_ASSUME_DEFAULT_BATTERY_MIN*60)/100;

   #ifdef IBAM_DEBUG
      cout << "Remaining percent: " << remainingBatteryPercent << endl;
      cout << "Remaining battery life seconds: " << remainingBatteryLifeSeconds << endl;
   #endif
}

inline void sysfs_status::update(void)
{
   ifstream in;
   DIR *sysfs_battery_dir;
   struct dirent *battery_entry;

   sysfs_battery_dir=opendir((Path).c_str());
   
   if (sysfs_battery_dir==NULL) 
   {
      acLineStatus = 0;
      chargeStatus = 0;
      remainingBatteryLifeSeconds = -1;
      remainingBatteryPercent = -1;
      return;
   }

   long total_capacity=0;
   long total_remain=0;
   long total_rate=0;
    
   while ((battery_entry=readdir(sysfs_battery_dir)))
   {
      if(battery_entry->d_name!=string(".") 
      && battery_entry->d_name!=string(".."))
      {
         in.open((((Path)+battery_entry->d_name)+"/present").c_str());
         int present=0,capacity=0,remain=0,rate=0;;
         if(!in.fail())
         {
            char c;
            in >> c;
            if(c=='1') // present
            {
               present=1;
            }
         }
         in.close();
         
         if(present)
         {
            in.open((((Path)+battery_entry->d_name)+"/charge_full").c_str());
            if(!in.fail())
            {
               in>>capacity;
               total_capacity+=capacity;
            }
            in.close();
         }
         
         if(present && capacity)
         {
            in.open((((Path)+battery_entry->d_name)+"/charge_now").c_str());
            if(!in.fail())
            {
               in>>remain;
               total_remain+=remain;
            }
            in.close();
         }

         if(present && capacity)
         {
            in.open((((Path)+battery_entry->d_name)+"/current_now").c_str());
            if(!in.fail())
            {
               in>>rate;
               total_rate+=rate;
            }
            in.close();
         }
         
         if(present && capacity)
         {
            in.open((((Path)+battery_entry->d_name)+"/status").c_str());
            if(!in.fail())
            {
               char c;//,d,e,f,g,h;
               in >> c; // >> d >> e >> f >> g >> h; // OUCH... #-} Somebody, please fix me
               if(c=='C') // charging state: Charging
               {
                  acLineStatus=1;
                  batteryStatus=3;
                  chargeStatus=1;
               } else
               if(c=='D') // charging state: Discharge
               {
                  acLineStatus=0;
                  batteryStatus=0;
                  chargeStatus=0;
               } else
               if(c=='F') // charging state: Full
               {
                  acLineStatus=1;
                  batteryStatus=0;
                  chargeStatus=0;
               }
            }
            in.close();
         }
      }
   }
   closedir(sysfs_battery_dir);

   if(total_capacity)
   {
      remainingBatteryPercent=int((100.*total_remain)/total_capacity+.5);
      remainingBatterySubPercent=100.*total_remain/total_capacity+.5-remainingBatteryPercent;
   }
   else
   {
      remainingBatteryPercent=100;
      remainingBatterySubPercent=0;
   }
            
   if(remainingBatteryPercent>100)
   {
      remainingBatteryPercent=100; // Don't ask...
      remainingBatterySubPercent=0;
   }

   if(remainingBatteryPercent<100 && acLineStatus==1 && chargeStatus==0) // Deal with strange Acpi-Data?
   {
      //  either
      // acLineStatus=1;
      // batteryStatus=3;
      // chargeStatus=1;
      //  or
      // nothing (or is it just occuring because of late last_full_capacity update?)
      //  or
      // since it seems it starts at 100% for discharge
      remainingBatteryPercent=100;
      remainingBatterySubPercent=0;
   }


   if(total_rate)
   {
      if(chargeStatus)
      {
         remainingBatteryLifeSeconds=int(((total_capacity-total_remain)*60.*60)/total_rate+.5);
         if(remainingBatteryLifeSeconds<0)
            remainingBatteryLifeSeconds=0;
      }
      else
         remainingBatteryLifeSeconds=int((total_remain*60.*60)/total_rate+.5);
   }
   else
      remainingBatteryLifeSeconds=(remainingBatteryPercent*IBAM_ASSUME_DEFAULT_BATTERY_MIN*60)/100;

   #ifdef IBAM_DEBUG
      cout << "Remaining percent: " << remainingBatteryPercent << endl;
      cout << "Remaining battery life seconds: " << remainingBatteryLifeSeconds << endl;
   #endif
}

inline void percent_data::size_to(int newpercents)
{
   if(newpercents>=maxpercents)
   {
      newpercents++;
      double *time_for=new double[newpercents];
      double *time_deriv=new double[newpercents];
      int    *samples=new int[newpercents];
      int i;
      for(i=0;i<maxpercents;i++)
      {
         time_for[i]=time_for_percent[i];
         time_deriv[i]=time_deriv_for_percent[i];
         samples[i]=time_samples[i];
      }
      for(;i<newpercents;i++)
         time_for[i]=time_deriv[i]=samples[i]=0;
      
      delete [] time_for_percent;
      delete [] time_deriv_for_percent;
      delete [] time_samples;
      time_for_percent=time_for;
      time_deriv_for_percent=time_deriv;
      time_samples=samples;
      maxpercents=newpercents;
   }
}   
   
inline percent_data::percent_data(void) : maxpercents(101), 
                  time_for_percent(new double[maxpercents]),
                  time_deriv_for_percent(new double[maxpercents]),
                  time_samples(new int[maxpercents]),
                  soft_low_limit(0),hard_low_limit(0)
{
   int i;
   for(i=0;i<maxpercents;i++)
      time_for_percent[i]=time_deriv_for_percent[i]=time_samples[i]=0;
}
inline percent_data::~percent_data(void)
{
   delete [] time_for_percent;
   delete [] time_deriv_for_percent;
   delete [] time_samples;
}
inline ostream & operator <<(ostream & o,const percent_data & a)
{
   int i;
   #ifndef NO_LOCALE_H
   setlocale(LC_ALL,"en_US");
   #endif
   for(i=a.maxpercents-1;i>=0;i--)
      if(a.time_samples[i])
      {
         if(a.time_deriv_for_percent[i]<0)
            a.time_deriv_for_percent[i]=0;
         o << i << '\t' << a.time_for_percent[i] << '\t' << sqrt(a.time_deriv_for_percent[i]) << '\t' << a.time_samples[i] << endl;
      }
   return o;
}
inline double percent_data::add_data(int percent,double time_for,int samples)
{
   if(percent<0)
      return 0;
   size_to(percent);
   double ratio;
   if(time_samples[percent])
      ratio=time_for/time_for_percent[percent];
   else
      ratio=time_for/(IBAM_ASSUME_DEFAULT_BATTERY_MIN*60./100.);
      
   double old_time_for_percent=time_for_percent[percent];
      
   time_for_percent[percent]=
    (time_for_percent[percent]*time_samples[percent]
    +time_for*samples
    )/(samples+time_samples[percent]);
    
   time_deriv_for_percent[percent]=
    ( (time_deriv_for_percent[percent]+old_time_for_percent*old_time_for_percent)*time_samples[percent]
    +time_for*time_for*samples
    )/(samples+time_samples[percent])-time_for_percent[percent]*time_for_percent[percent];
    
   time_samples[percent]+=samples;
   return ratio;
}
inline double percent_data::average(int a,int b) // average from a to b
{
   if(a>b) { int c=a;a=b;b=c; }
   if(a<0)
   {
      a=0;
      if(b<0)
         b=0;
   }
   if(b>=maxpercents)
   {
      b=maxpercents-1;
      if(a>=maxpercents)
         a=b;
   }
   int i;
   double su(0);
   int    co(0);
   for(i=a;i<=b;i++)
   {
      if(time_samples[i])
      {
         su+=time_for_percent[i]*time_samples[i];
         co+=time_samples[i];
      }
   }
   if(co)
      return (su/co);
   int gotdata=0;
   for(a--,b++;(a>0 || b<maxpercents-1) && gotdata<2;a--,b++)
   {
      if(a<0)
         a=0;
      if(b>=maxpercents)
         b=maxpercents-1;
      su+=time_for_percent[a]*time_samples[a]
          +time_for_percent[b]*time_samples[b];
      co+=time_samples[a]+time_samples[b];
      if(time_samples[a] || time_samples[b])
         gotdata++;
   }
   if(co)
      return (su/co);

   return (IBAM_ASSUME_DEFAULT_BATTERY_MIN*60/100);
}

inline double percent_data::add_data(int percent,double time_for,double time_deriv_for,int samples)
{
   if(percent<0)
      return 0;
   size_to(percent);
   double ratio;
   if(time_samples[percent])
      ratio=time_for/time_for_percent[percent];
   else
      ratio=time_for/average(percent,percent);
      
   double old_time_for_percent=time_for_percent[percent];
      
   time_for_percent[percent]=
    (time_for_percent[percent]*time_samples[percent]
    +time_for*samples
    )/(samples+time_samples[percent]);
    
   time_deriv_for_percent[percent]=
    ( (time_deriv_for_percent[percent]+old_time_for_percent*old_time_for_percent)*time_samples[percent]
    + (time_deriv_for+time_for*time_for)*samples
    )/(samples+time_samples[percent])-time_for_percent[percent]*time_for_percent[percent];
    
   time_samples[percent]+=samples;
   return ratio;
}
inline istream & operator >>(istream & i,percent_data &a)
{
   #ifndef NO_LOCALE_H
   setlocale(LC_ALL,"en_US");
   #endif

   while(!i.fail() && !i.eof())
   {
      int percent;
      double time_for(-1);
      double time_deriv_for(-1);
      int samples;
      i >> percent >> time_for >> time_deriv_for>> samples;
      if(time_for>=0)
         a.add_data(percent,time_for,time_deriv_for*time_deriv_for,samples);
   }
   return i;
}
inline istream & percent_data::import(istream & i)
{
   #ifndef NO_LOCALE_H
   setlocale(LC_ALL,"en_US");
   #endif

   percent_data & a(*this);
   double maxval=0;
   while(!i.fail() && !i.eof())
   {
      int val;
      double time_for(-1);
      int samples;
      i >> val >> time_for >> samples;
      if(val>maxval)
         maxval=val;
      if(time_for>=0)
         a.add_data(int(double(val)/maxval*100+.5),time_for*maxval/100,samples/10+1);
   }
   return i;
}
inline double percent_data::remain(int percent)
{
   double r=0;
   size_to(percent);
   int i;
   for(i=percent;i>0 && i>soft_low_limit && i>hard_low_limit;i--)
   {
      if(time_samples[i])
         r+=time_for_percent[i];
      else
      {
         int down=i-15;
         int up=i+15;
         if(down<0)
            down=0;
         if(up>=maxpercents)
            up=maxpercents-1;
         r+=average(down,up);
      }
   }
   return r;
}
inline double percent_data::inverted_remain(int percent)
{
   double r=0;
   size_to(percent);
   int i;
   for(i=percent+1;i<maxpercents;i++)
   {
      if(time_samples[i])
         r+=time_for_percent[i];
      else
      {
         int down=i-15;
         int up=i+15;
         if(down<0)
            down=0;
         if(up>=maxpercents)
            up=maxpercents-1;
         r+=average(down,up);
      }
   }
   return r;
}
inline double percent_data::total(void)
{
   double r=0;
   int i;
   for(i=maxpercents-1;i>0 && i>soft_low_limit && i>hard_low_limit;i--)
   {
      if(time_samples[i])
         r+=time_for_percent[i];
      else
      {
         int down=i-15;
         int up=i+15;
         if(down<0)
            down=0;
         if(up>=maxpercents)
            up=maxpercents-1;
         r+=average(down,up);
      }
   }
   return r;
}

inline int percent_data::data_low_limit(void)
{
   int i;
   for(i=1;i<maxpercents && !time_samples[i];i++);
   return i;
}

inline void percent_data::set_soft_low_limit(int a) { soft_low_limit=a; }
inline void percent_data::set_hard_low_limit(int a) { hard_low_limit=a; }

inline ibam::ibam(const string &aHome) : 
             data_changed(0),
             battery_loaded(0),battery_changed(0),
             charge_loaded(0),charge_changed(0),
             profile_changed(0),
             lasttime(time(NULL)),lastpercent(0),
             lastratio(1),lastratiocount(1),
             laststatus(-1),
             currenttime(time(NULL)),isvalid(0),profile_logging(1),
             profile_number(0),profile_active(0),
             soft_low_limit(5),hard_low_limit(0)
{
   string pmu_path = "/proc/pmu";    // These strings are already in ibam.hpp,
   string acpi_path = "/proc/acpi";  // maybe a static function should check this
   string sysfs_path = "/sys/class/power_supply"; // ...
   ifstream pmu,acpi,sysfs;
   pmu.open((pmu_path+"/info").c_str());
   acpi.open((acpi_path+"/info").c_str());
   if (pmu.is_open()) {
#ifdef IBAM_DEBUG
      cout << "using pmu" << endl;
#endif
      pmu.close();
      apm = new pmu_status();
   } else if (acpi.is_open()) {
#ifdef IBAM_DEBUG
      cout << "using acpi" << endl;
#endif
      acpi.close();
      apm = new acpi_status();
   } else {
      sysfs.open((sysfs_path+"/BAT1/charge_full").c_str());
      if(sysfs.is_open()) {
#ifdef IBAM_DEBUG
      cout << "using sysfs" << endl;
#endif
         apm = new sysfs_status();
      } else
      {
#ifdef IBAM_DEBUG
         cout << "using apm" << endl;
#endif
         apm = new apm_status();
      }
   }

   home=aHome; // directory must exist, no trailing slash

   #ifndef NO_MKDIR
   if(home=="")
   {
      home=getenv("HOME");
      if(home!="")
         home+="/";
      mkdir((home+".ibam").c_str(),0755);
      home+=".ibam";
   }
   #endif
   ifstream in((home+"/ibam.rc").c_str());
   string saveversion;
   in >> saveversion;
   double dummy;
   if(saveversion==string("0.3"))
   {
      in >> lasttime >> lastpercent >> lastratio >> laststatus >> dummy >> dummy >> profile_logging >> profile_number >> profile_active;
   }
   if(saveversion==string("0.4"))
   {
      in >> lasttime >> lastpercent >> lastratio >> lastratiocount >> laststatus >> profile_logging >> profile_number >> profile_active;
   }
   if(saveversion==string("0.5") || saveversion==string("0.5.1") || saveversion==string("0.5.2"))
   {
      in >> lasttime >> lastpercent >> lastratio >> lastratiocount >> laststatus >> profile_logging >> profile_number >> profile_active >> soft_low_limit >> hard_low_limit;
   } else
      data_changed=1; // force update
   in.close();
   
   currentpercent=apm->percent();
   if(currentpercent!=-1)
      isvalid=1;

   currentstatus=apm->onBattery()?1:apm->charging()?2:0;

   if(currentstatus!=laststatus)
   {
      lastratio=1;
      lastratiocount=1;
   }
}

inline void ibam::update(void)
{
   save();
   apm->update();
   currenttime=time(NULL);
   currentpercent=apm->percent();
   if(currentpercent!=-1)
      isvalid=1;
   else
      isvalid=0;
      
   currentstatus=apm->onBattery()?1:apm->charging()?2:0;

   if(currentstatus!=laststatus)
   {
      lastratio=1;
      lastratiocount=1;
   }
}

inline int  ibam::valid(void) const { return isvalid; }

inline void ibam::import(void)
{
   {
      ifstream in(".ibam.battery.rc");
      battery.import(in);
      battery_changed=1;
   }
   {
      ifstream in(".ibam.charge.rc");
      charge.import(in);
      charge_changed=1;
   }
}

inline void ibam::load_battery(void)
{
   if(!battery_loaded)
   {
      ifstream in((home+"/battery.rc").c_str());
      in >> battery;
      if(battery.data_low_limit()<=soft_low_limit)
      {
         soft_low_limit=battery.data_low_limit()-1;
         data_changed=1;
      }
      battery.set_soft_low_limit(soft_low_limit);
      battery.set_hard_low_limit(hard_low_limit);
      battery_loaded=1;
   }
}

inline void ibam::load_charge(void)
{
   if(!charge_loaded)
   {
      ifstream in((home+"/charge.rc").c_str());
      in >> charge;
      charge_loaded=1;
   }
}

inline void ibam::update_statistics(void)
{

#ifdef EXPERIMENTAL
   int remember_current=currentstatus;
   int remember_last=laststatus;

   // Many batteries switch to charged state immediatly when hitting 100%,
   // this way, the 99->100% step never gets recorded. The next lines, check
   // whether the state has just changed, and assume once, that we are still
   // charging- this way the last step will be measured. The same applies
   // when unplugging the power cable.
   //
   // The problem is, that this data is highly inaccurate as it is unclear
   // when ibam ran for the last time- this is not stored as this would lead
   // to continuous harddisc usage.

   if( (laststatus==2 && (currentstatus!=1 && currentstatus!=2)) // was charging, then full
    || ((laststatus!=1 && laststatus!=2) && currentstatus==1) // was full, then on battery 
     )
   {
      if(currentpercent!=lastpercent) // There is data at all...
      {
         if(laststatus==2) currentstatus=2; // Assume once that we are still charging
         if(currentstatus==1) laststatus=1; // Assume once that we just switched to battery
      }
   }
#endif

   if(currentstatus==laststatus && 
      currenttime-lasttime<IBAM_IGNORE_DATA_AFTER_X_SECONDS)
   {
      switch(currentstatus)
      {
         case 1: // on battery
            if(currentpercent==lastpercent+1) 
               currentpercent=lastpercent; // minor fluctuation ignored

            if(currentpercent<lastpercent)
            {
               load_battery();
               double sec_per_min=(currenttime-lasttime)/double(lastpercent-currentpercent);
               double last_av=battery.average(currentpercent,lastpercent);
               
               if(sec_per_min>=IBAM_MINIMAL_SECONDS_PER_PERCENT 
               && sec_per_min<=IBAM_MAXIMAL_SECONDS_PER_PERCENT)
               {
                  int i;
                  last_sec_per_min=sec_per_min;
                  last_sec_per_min_prediction=last_av;
                  profile_changed=1;

                  if(lastpercent-currentpercent>lastratiocount)
                     lastratiocount=(lastpercent-currentpercent);
                  
                  for(i=currentpercent;i<=lastpercent;i++)
                  {
                     if(lastratiocount>2 && lastpercent!=100) // Don't trust the first
                        lastratio=(lastratio*lastratiocount+battery.add_data(i,sec_per_min))/(lastratiocount+1);
                     lastratiocount++;
                  }

                  battery_changed=1;
                  data_changed=1;
               }              
            } else
            if(currentpercent>lastpercent) // strange data
            {
               data_changed=1; // discard
               if(profile_logging && profile_active)
                  profile_number++;
               profile_active=0;
            }
            break;
         case 2: // charging
            if(currentpercent>lastpercent)
            {
               load_charge();
               double sec_per_min;
               sec_per_min=(currenttime-lasttime)/double(currentpercent-lastpercent);
               double last_av=charge.average(lastpercent,currentpercent);
               
               if(sec_per_min<=IBAM_MAXIMAL_SECONDS_PER_PERCENT 
               && sec_per_min>=IBAM_MINIMAL_SECONDS_PER_PERCENT)
               {
                  int i;
                  last_sec_per_min=sec_per_min;
                  last_sec_per_min_prediction=last_av;
                  profile_changed=1;
                  
                 if(currentpercent-lastpercent>lastratiocount)
                     lastratiocount=(currentpercent-lastpercent);

                  for(i=lastpercent;i<=currentpercent;i++)
                  {
                     if(lastratiocount>2) // Don't trust the first
                        lastratio=(lastratio*lastratiocount+1./charge.add_data(i,sec_per_min))/(lastratiocount+1);
                     lastratiocount++;
                  }
 
                  charge_changed=1;
                  data_changed=1;
               }
            } else
            if(currentpercent<lastpercent) // strange data
            {
               if(profile_logging && profile_active)
                  profile_number++;
               profile_active=0;

               data_changed=1; // discard
            }
            break;
         default: // full or no battery
            break;
      }
   } 

#ifdef EXPERIMENTAL
   currentstatus=remember_current;
   laststatus=remember_last;
#endif

   if(currentstatus!=laststatus || 
      currenttime-lasttime>=IBAM_IGNORE_DATA_AFTER_X_SECONDS)
   {
      if(profile_logging && profile_active)
         profile_number++;
      profile_active=0;
      data_changed=1;
   }
}

inline void ibam::ignore_statistics(void)
{
   data_changed=1;
}

inline string ibam::profile_filename(int n,int type) const
{
   char b[20];
   char *status_text[4]={"full","battery","charge",""};
   sprintf(b,"profile-%03d-%s",n,status_text[(type&3)]);
   return (home+"/")+b;
}

inline int   ibam::current_profile_number(void) const { return profile_number; }
inline int   ibam::current_profile_type(void) const { return currentstatus; }

inline void ibam::save(void)
{
   if(profile_changed && profile_logging)
   {
      profile_number%=IBAM_MAXIMAL_PROFILES;
      string filename=profile_filename(profile_number,currentstatus);
      ofstream out(filename.c_str(),ios::app);
      out << currentpercent << '\t' << last_sec_per_min << '\t' << last_sec_per_min_prediction << endl;
      if(profile_active==0)
         data_changed=1;
      profile_active=1;
      profile_changed=0;
   }
   if(battery_changed)
   {
      ofstream out((home+"/battery.rc").c_str());
      out << battery;
      battery_changed=0;
   }
   if(charge_changed)
   {
      ofstream out((home+"/charge.rc").c_str());
      out << charge;
      charge_changed=0;
   }
   if(data_changed)
   {
      ofstream out((home+"/ibam.rc").c_str());

      if(currentpercent<=soft_low_limit)
         soft_low_limit=currentpercent-1;

      out << IBAM_VERSION 
          << '\t' << currenttime 
          << '\t' << currentpercent 
          << '\t' << lastratio 
          << '\t' << lastratiocount
          << '\t' << currentstatus 
          << '\t' << profile_logging 
          << '\t' << profile_number 
          << '\t' << profile_active 
          << '\t' << soft_low_limit
          << '\t' << hard_low_limit 
          << endl;
      lasttime=currenttime;
      lastpercent=currentpercent;
      laststatus=currentstatus;
      data_changed=0;
   }
}

inline void  ibam::set_profile_logging(int a)          { data_changed|=(a!=profile_logging);profile_logging=a; }
inline int   ibam::profile_logging_setting(void) const { return profile_logging; }

inline void  ibam::set_soft_low_limit(int a)           { data_changed|=(a!=soft_low_limit);soft_low_limit=a; }
inline int   ibam::get_soft_low_limit(void) const      { return soft_low_limit; }
inline void  ibam::set_hard_low_limit(int a)           { data_changed|=(a!=hard_low_limit);hard_low_limit=a; }
inline int   ibam::get_hard_low_limit(void) const      { return hard_low_limit; }
      
inline int   ibam::seconds_left_battery_bios(void)     { return apm->seconds(); }
inline int   ibam::seconds_left_battery(void)          { load_battery(); return int(battery.remain(currentpercent)+.5); }
inline int   ibam::seconds_left_battery_adaptive(void) { load_battery(); return int(battery.remain(currentpercent)*lastratio+.5); }

inline int   ibam::percent_battery_bios(void)          { return apm->percent(); }
inline int   ibam::percent_battery(void)               { load_battery(); return int((100.*seconds_left_battery())/battery.total()+.5); }
            
inline int   ibam::seconds_left_charge(void)           { load_charge(); return int(charge.inverted_remain(currentpercent)+.5); }
inline int   ibam::seconds_left_charge_adaptive(void)  { load_charge(); return int(charge.inverted_remain(currentpercent)/lastratio+.5); }

inline int   ibam::percent_charge(void)                { load_charge(); return 100-int((100.*seconds_left_charge())/charge.total()+.5); }

inline int   ibam::seconds_battery_total(void)         { load_battery(); return int(battery.total()+.5); }
inline int   ibam::seconds_battery_total_adaptive(void){ load_battery(); return int(battery.total()*lastratio+.5); }

inline int   ibam::seconds_charge_total(void)          { load_charge(); return int(charge.total()+.5); }
inline int   ibam::seconds_charge_total_adaptive(void) { load_charge(); return int(charge.total()/lastratio+.5); }

inline int   ibam::seconds_battery_correction_adaptive(void) { return seconds_battery_correction(lastratio); }

inline int   ibam::seconds_battery_correction(double ratio)
{
   if(currentstatus!=laststatus || currentstatus==0
    || lastpercent!=currentpercent)
      return 0;
   if(currentstatus==1)
   {
      if(apm->subpercent()!=-1)
      {
         load_battery();
         float v=apm->subpercent();
         return -int((1-apm->subpercent())*battery.average(currentpercent,currentpercent)*ratio*(1-v)+(currenttime-lasttime)*v+.5);
      }
      return lasttime-currenttime;
   }
   load_battery();
   load_charge();
   return int((currenttime-lasttime)*(battery.average(currentpercent-1,currentpercent+1)/charge.average(currentpercent-1,currentpercent+1))+.5);
}

inline int   ibam::seconds_charge_correction_adaptive(void) { return seconds_charge_correction(lastratio); }

inline int   ibam::seconds_charge_correction(double ratio)
{
   if(currentstatus!=laststatus || currentstatus==0
    || lastpercent!=currentpercent)
      return 0;
   if(currentstatus==2)
   {
      if(apm->subpercent()!=-1)
      {
         load_battery();
         float v=1-apm->subpercent();
         return -int((apm->subpercent())*charge.average(currentpercent,currentpercent)/ratio*(1-v)+(currenttime-lasttime)*v+.5);
      }
      return lasttime-currenttime;
   }
   load_battery();
   load_charge();
   return int((currenttime-lasttime)/(battery.average(currentpercent-1,currentpercent+1)/charge.average(currentpercent-1,currentpercent+1))+.5);
}

inline int   ibam::onBattery(void) { return apm->onBattery(); }
inline int   ibam::charging(void)  { return apm->charging(); }

inline double percent_data::average_derivation(int a,int b) // average standard derivation from a to b
{
   if(a>b) { int c=a;a=b;b=c; }
   if(a<0)
   {
      a=0;
      if(b<0)
         b=0;
   }
   if(b>=maxpercents)
   {
      b=maxpercents-1;
      if(a>=maxpercents)
         a=b;
   }
   int i;
   double su(0);
   int    co(0);
   for(i=a;i<=b;i++)
   {
      if(time_samples[i])
      {
         if(time_deriv_for_percent[i]>0)
            su+=sqrt(time_deriv_for_percent[i])*time_samples[i];
         co+=time_samples[i];
      }
   }
   if(co)
      return (su/co);
   int gotdata=0;
   for(a--,b++;(a>0 || b<maxpercents-1) && gotdata<2;a--,b++)
   {
      if(a<0)
         a=0;
      if(b>=maxpercents)
         b=maxpercents-1;
      if(time_deriv_for_percent[a]>0 && time_samples[a])
         su+=sqrt(time_deriv_for_percent[a])*time_samples[a];
      if(time_deriv_for_percent[b]>0 && time_samples[b])
         su+=sqrt(time_deriv_for_percent[b])*time_samples[b];
      co+=time_samples[a]+time_samples[b];
      if(time_samples[a] || time_samples[b])
         gotdata++;
   }
   if(co)
      return (su/co);

   return 20;
}


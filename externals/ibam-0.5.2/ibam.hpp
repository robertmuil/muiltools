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

#define IBAM_IGNORE_DATA_AFTER_X_SECONDS  3600
#define IBAM_MINIMAL_SECONDS_PER_PERCENT  10
#define IBAM_MAXIMAL_SECONDS_PER_PERCENT  800
#define IBAM_ASSUME_DEFAULT_BATTERY_MIN   120
#define IBAM_MAXIMAL_PROFILES             500

#include <iostream>
#include <fstream>
#include <string>
#include <math.h>
#include <stdlib.h>
#include <unistd.h>
#include <time.h>

#ifdef WITH_IBAM
   // pbbuttons detection
   #define NO_LOCALE_H
   #define NO_MKDIR
#endif

using namespace std;

class battery_status
{
   protected:
      int acLineStatus;
      int batteryStatus;
      int chargeStatus;
      int remainingBatteryPercent;
      float remainingBatterySubPercent;
      int remainingBatteryLifeSeconds;
      string Path;
   public:
      inline int   onBattery(void) const;
      inline int   charging(void)  const;
      inline int   percent(void)   const;
      inline float subpercent(void) const;
      inline int   seconds(void)   const;
      virtual inline void update(void) = 0;
     inline battery_status(string path);
     virtual inline ~battery_status(void);
};

class apm_status : public battery_status
{
   public:
      inline void update(void);
      inline apm_status(string path="/proc/apm");
};

class pmu_status : public battery_status
{
   public:
      inline void update(void);
      inline pmu_status(string path="/proc/pmu");
};
      
class acpi_status : public battery_status
{
   public:
      inline void update(void);
      inline acpi_status(string path="/proc/acpi");
};
      
class sysfs_status : public battery_status
{
   public:
      inline void update(void);
      inline sysfs_status(string path="/sys/class/power_supply/");
};
      
class percent_data
{
   private:
      int      maxpercents;
      double  *time_for_percent;
      double  *time_deriv_for_percent;
      int     *time_samples;
      int      soft_low_limit,hard_low_limit;
      
      inline void size_to(int newpercents);
   
   public:
      inline percent_data(void);
      inline ~percent_data(void);
      friend inline ostream & operator <<(ostream & o,const percent_data & a);
      inline double add_data(int percent,double time_for,int samples=1);
      inline double average(int a,int b); // average from a to b
      inline double average_derivation(int a,int b); // standard derivation from a to b
      inline double add_data(int percent,double time_for,double time_deriv_for,int samples=1);
      friend inline istream & operator >>(istream & i,percent_data &a);
      inline istream & import(istream & i);
      inline double remain(int percent);
      inline double inverted_remain(int percent);
      inline double total(void);
      inline int  data_low_limit(void);
      inline void set_soft_low_limit(int);
      inline void set_hard_low_limit(int);
};

class ibam
{
   private:
      percent_data data;
      int         data_changed;    // 1 if save of ibam.rc demanded
      battery_status  *apm;
      percent_data battery;
      int         battery_loaded;
      int         battery_changed;
      percent_data charge;
      int         charge_loaded;
      int         charge_changed;
      int         profile_changed;
      
      unsigned long  lasttime;
      int            lastpercent;
      double         lastratio;
      int            lastratiocount;
      int            laststatus;
      
      double         last_sec_per_min;
      double         last_sec_per_min_prediction;
      
      unsigned long  currenttime;
      int            currentpercent;
      int            currentstatus;
      
      string     home;
      
      int            isvalid;
      
      int            profile_logging; // 1 if cycle shall be logged for later analysis
      int            profile_number;  // number of profile (increased on each cycle change)
      int            profile_active;  // data has been written to current profile
      int            soft_low_limit;  // minimum percentage observed and therefore lowest safe value
      int            hard_low_limit;  // minimum percentage found safe by user

   public:
      #ifdef NO_MKDIR
      inline ibam(const string &);
      #else
      inline ibam(const string &a="");
      #endif
      inline void import(void);
      inline void load_battery(void);
      inline void load_charge(void);
      inline void update_statistics(void);
      inline void ignore_statistics(void);
      inline void save(void);
      inline string profile_filename(int n,int type) const;
      inline int   current_profile_number(void) const;
      inline int   current_profile_type(void) const;

      inline void  set_profile_logging(int);
      inline int   profile_logging_setting(void) const;
      
      inline void  set_soft_low_limit(int);
      inline int   get_soft_low_limit(void) const;
      inline void  set_hard_low_limit(int);
      inline int   get_hard_low_limit(void) const;
      
      inline int   seconds_left_battery_bios(void);
      inline int   seconds_left_battery(void);
      inline int   seconds_left_battery_adaptive(void);

      inline int   percent_battery_bios(void);
      inline int   percent_battery(void);
                  
      inline int   seconds_left_charge(void);
      inline int   seconds_left_charge_adaptive(void);

      inline int   percent_charge(void);
      
      inline int   seconds_battery_total(void);
      inline int   seconds_battery_total_adaptive(void);

      inline int   seconds_charge_total(void);
      inline int   seconds_charge_total_adaptive(void);
      
      inline int   seconds_battery_correction(double ratio=1);
      inline int   seconds_charge_correction(double ratio=1);
      inline int   seconds_battery_correction_adaptive(void);
      inline int   seconds_charge_correction_adaptive(void);

      inline int   onBattery(void);
      inline int   charging(void);
      
      inline int   valid(void) const;
      
      inline void  update(void);
};

#include "ibam.inl"

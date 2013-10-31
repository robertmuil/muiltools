// IBAM, the Intelligent Battery Monitor
// Copyright (C) 2001-2005, Sebastian Ritterbusch (IBAM@Ritterbusch.de)
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

#include "ibam.hpp"
#include <getopt.h>

#include <sys/stat.h>  // for mkdir
#include <sys/types.h> // for mkdir

int no_HMS=0;

class HMS
{
   private: int secs;
   public:  HMS(int s) : secs(s) { if(secs<0) secs=0; }
      friend ostream & operator <<(ostream & o,const HMS & a)
      {
         if(no_HMS)
            return (o << a.secs);
         o.fill(' ');
         o.width(2);
         o << a.secs/3600 << ':';
         o.width(2);
         o.fill('0');
         o << (a.secs/60)%60 << ':';
         o.width(2);
         o.fill('0');
         o << a.secs % 60;
         return o;  
      }
};

int main(int argc,char *argv[])
{
   ibam data;
   
   int   show_minimal=1;
   int   show_bios=0;
   int   show_seconds_left_battery_bios=0;
   int   show_seconds_left_battery=0;
   int   show_seconds_left_battery_adaptive=0;
   int   show_percent_battery_bios=0;
   int   show_percent_battery=0;
   int   show_seconds_left_charge=0;
   int   show_seconds_left_charge_adaptive=0;
   int   show_percent_charge=0;
   int   show_seconds_battery_total=0;
   int   show_seconds_battery_total_adaptive=0;
   int   show_seconds_charge_total=0;
   int   show_seconds_charge_total_adaptive=0;
   int   show_profile_logging=0;
   int   show_credits=0;
   int   do_second_correction=0;
   int   show_soft_low_limit=0;
   int   show_hard_low_limit=0;
   
   int   readonly = 0;
   
   string   home(getenv("HOME"));
   if(home!="")
      home+="/";
   
   while(1)
   {
      int   option_index=0;
      static struct option long_options[] =
      {
         {"bios",0,0,'b'},
         {"help",0,0,'h'},
         {"batterybios",0,0,0},
         {"battery",0,0,1},
         {"batteryadaptive",0,0,2},
         {"percentbios",0,0,3},
         {"percentbattery",0,0,4},
         {"charge",0,0,5},
         {"chargeadaptive",0,0,6},
         {"percentcharge",0,0,7},
         {"totalbattery",0,0,8},
         {"totalbatteryadaptive",0,0,9},
         {"totalcharge",0,0,10},
         {"totalchargeadaptive",0,0,11},
         {"plot",optional_argument,0,12},
         {"plotderivations",optional_argument,0,13},
         {"import",0,0,14},
         {"correctseconds",0,0,'c'},
         {"seconds",0,0,'s'},
         {"readonly",0,0,'r'},
         {"all",0,0,'a'},
         {"version",0,0,'v'},
         {"profile",0,0,15},
         {"noprofile",0,0,16},
         {"credits",0,0,17},
         {"softlowlimit",optional_argument,0,18},
         {"hardlowlimit",optional_argument,0,19},
         {0,0,0,0}         
      };
      int c=getopt_long(argc,argv,"avbhcsr",long_options,&option_index);
      if(c==-1)
         break;
      switch(c)
      {
         case 0: show_seconds_left_battery_bios=1; break;
         case 1: show_seconds_left_battery=1; break;
         case 2: show_seconds_left_battery_adaptive=1;break;
         case 3: show_percent_battery_bios=1;break;
         case 4: show_percent_battery=1;break;
         case 5: show_seconds_left_charge=1;break;
         case 6: show_seconds_left_charge_adaptive=1;break;
         case 7: show_percent_charge=1;break;
         case 8: show_seconds_battery_total=1;break;
         case 9: show_seconds_battery_total_adaptive=1;break;
         case 10: show_seconds_charge_total=1;break;
         case 11: show_seconds_charge_total_adaptive=1;break;
         case 12: 
            {
               string command;
               command=string("echo \"plot \\\"")
                  +home
                  +string(".ibam/battery.rc\\\" using 1:2 title \\\"Battery\\\" with lines,\\\"")
                  +home
                  +string(".ibam/charge.rc\\\" using 1:2 title \\\"Charge\\\" with lines");
               if (optarg)
               {
                  int n=atoi(optarg);
                  if(n>IBAM_MAXIMAL_PROFILES)
                     n=IBAM_MAXIMAL_PROFILES;
                  int p=data.current_profile_number();
                  for(;n>=0;n--)
                  {
                     string batname=data.profile_filename(p,1);
                     string chrname=data.profile_filename(p,2);
                     ifstream batteryprofile(batname.c_str());
                     if(!batteryprofile.fail())
                     {
                        command+=", \\\""+batname+"\\\" using 1:2 notitle with lines 5";
                     } else
                     {
                        ifstream chargeprofile(chrname.c_str());
                        if(!chargeprofile.fail())
                        {
                           command+=", \\\""+chrname+"\\\" using 1:2 notitle with lines 6";
                        }
                     }
                     p--;
                     if(p<0)
                        p+=IBAM_MAXIMAL_PROFILES;
                  }
                  
               }

               
               command+="\" | gnuplot -persist";
               system(command.c_str());
            }
            break;
         case 13:
            { 
               string command;
               command=string("echo \"plot \\\"")
                  +home
                  +string(".ibam/battery.rc\\\" using 1:2 title \\\"Battery\\\" with lines 1, \\\"")
                  +home
                  +string(".ibam/battery.rc\\\" using 1:(\\$2+\\$3) notitle with lines 3, \\\"")
                  +home
                  +string(".ibam/battery.rc\\\" using 1:(\\$2-\\$3) notitle with lines 3,\\\"")
                  +home
                  +string(".ibam/charge.rc\\\" using 1:2 title \\\"Charge\\\" with lines 2, \\\"")
                  +home
                  +string(".ibam/charge.rc\\\" using 1:(\\$2+\\$3) notitle with lines 4, \\\"")
                  +home
                  +string(".ibam/charge.rc\\\" using 1:(\\$2-\\$3) notitle with lines 4");
               if (optarg)
               {
                  int n=atoi(optarg);
                  if(n>IBAM_MAXIMAL_PROFILES)
                     n=IBAM_MAXIMAL_PROFILES;
                  int p=data.current_profile_number();
                  for(;n>=0;n--)
                  {
                     string batname=data.profile_filename(p,1);
                     string chrname=data.profile_filename(p,2);
                     ifstream batteryprofile(batname.c_str());
                     if(!batteryprofile.fail())
                     {
                        command+=", \\\""+batname+"\\\" using 1:2 notitle with lines 5";
                     } else
                     {
                        ifstream chargeprofile(chrname.c_str());
                        if(!chargeprofile.fail())
                        {
                           command+=", \\\""+chrname+"\\\" using 1:2 notitle with lines 6";
                        }
                     }
                     p--;
                     if(p<0)
                        p+=IBAM_MAXIMAL_PROFILES;
                  }
                  
               }
               command+="\" | gnuplot -persist";
               system(command.c_str());
            }
            break;
         case 14:
            data.import();
            break;
         case 15:
            data.set_profile_logging(1);
            break;
         case 16:
            data.set_profile_logging(0);
            break;
         case 17:
            show_credits=1;
            break;
         case 'c': do_second_correction=1; break;
         case 'b': show_bios=1; break;
         case 's': no_HMS=1; break;
         case 'r': readonly=1; break;
         case 'a': show_soft_low_limit=show_hard_low_limit=show_profile_logging=show_seconds_left_battery_bios=show_seconds_left_battery=show_seconds_left_battery_adaptive=show_percent_battery_bios=show_percent_battery=show_seconds_left_charge=show_seconds_left_charge_adaptive=show_percent_charge=show_seconds_battery_total=show_seconds_battery_total_adaptive=show_seconds_charge_total=show_seconds_charge_total_adaptive=1; break;
         case 'v': cerr << "IBAM-" << IBAM_VERSION << " (C) 2001-2008 Sebastian Ritterbusch" << endl; break;
         case 'h': 
            cout << "IBAM-" << IBAM_VERSION << ", the Intelligent Battery Monitor" << endl;
            cout << "(C) 2001-2008 Sebastian Ritterbusch" << endl << endl;
            cout << "Usage: ibam [options]" << endl;
            cout << endl;
            cout << "Options:" << endl;
            cout << "   -h, --help                 displays this message" << endl;
            cout << "   -v, --version              displays software version" << endl;
            cout << "   -b, --bios                 show bios apm guesses" << endl;
            cout << "   -s, --seconds              displays times in seconds" << endl;
            cout << "   -c, --correctseconds       displays changes in seconds" << endl;
            cout << "   -r, --readonly             no files will be updated" << endl;
            cout << "   -a, --all                  show ALL information" << endl;      
            cout << "       --battery              show battery time" << endl;
            cout << "       --batteryadaptive      show adaptive battery time" << endl;  
            cout << "       --batterybios          show bios battery time guess" << endl;
            cout << "       --percentbattery       show battery percentage" << endl;
            cout << "       --percentbios          show bios percentage" << endl;
            cout << "       --charge               show charge time" << endl;
            cout << "       --chargeadaptive       show adaptive charge time" << endl;
            cout << "       --percentcharge        show charge percentage" << endl;
            cout << "       --totalbattery         show total battery time" << endl;
            cout << "       --totalbatteryadaptive show adaptive total battery" << endl;
            cout << "       --totalcharge          show total charge time" << endl;
            cout << "       --totalchargeadaptive  show adaptive total charge" << endl;
            cout << "       --hardlowlimit[=lim]   show user defined hard lower percentage limit" << endl;
            cout << "                              [and set it to value <lim> or disable <0> it]" << endl;
            cout << "       --softlowlimit[=lim]   show automatic lower percentage limit" << endl;
            cout << "                              [and lower it to value <lim> or diable <0> it]" << endl;
            cout << "       --plot[=profiles]      use gnuplot to plot battery and charge graphs" << endl;
            cout << "                              and plot the last <profiles> additional profiles" << endl; 
            cout << "       --plotderivations[=profiles] same as above plus standard derivations" << endl;
            cout << "       --import               import V0.1 data from current directory" << endl;
            cout << "       --profile              enable additional yet unused profiling" << endl;
            cout << "       --noprofile            disable additional profiling" << endl;
            cout << "       --credits              to everyone contributing to ibam"<<endl;
            cout << endl;
            break;
         case 18:
            show_soft_low_limit=1;
            if (optarg)
            {
               int n=atoi(optarg);
               data.set_soft_low_limit(n);
            } 
            break;
         case 19:
            show_hard_low_limit=1;
            if (optarg)
            {
               int n=atoi(optarg);
               data.set_hard_low_limit(n);
            } 
            break;
      }
   };

   if(!data.valid())
   {
      cerr << "No apm data available." << endl;
      return 0;
   }

   if(!readonly)
   {
      data.update_statistics();
      data.save();
   }
   
   if(show_minimal)
   {
      if(data.onBattery())
         show_seconds_left_battery_adaptive=show_seconds_left_battery=1;
      else if(data.charging())
         show_seconds_left_charge=show_seconds_left_charge_adaptive=1;
      else
         show_seconds_charge_total=show_seconds_battery_total=1;
   }
   
   if(show_bios)
   {
      if(data.seconds_left_battery_bios()>=0)
         show_seconds_left_battery_bios=1;
      else
         show_percent_battery_bios=1;
   }
   
   if(show_percent_battery_bios)
      cout << "Bios percentage:            " << data.percent_battery_bios() << " %" << endl;
   
   if(show_percent_battery)
      cout << "Battery percentage:         " << data.percent_battery() << " %" << endl;      
   
   if(show_soft_low_limit && data.get_soft_low_limit()>0)
      cout << "Soft low percentage limit:  " << data.get_soft_low_limit() << " %" << endl;      
   
   if(show_hard_low_limit && data.get_hard_low_limit()>0)
      cout << "Hard low percentage limit:  " << data.get_hard_low_limit() << " %" << endl;      
   
   if(show_percent_charge)
      cout << "Charge percentage:          " << data.percent_charge() << " %" << endl;      
   
   if(show_seconds_left_battery_bios && data.seconds_left_battery_bios()>=0)
      cout << "Bios time left:             " << HMS(data.seconds_left_battery_bios()) << endl;
      
   if(show_seconds_left_battery && !do_second_correction)
      cout << "Battery time left:          " << HMS(data.seconds_left_battery()) << endl;

   if(show_seconds_left_battery && do_second_correction)
      cout << "Battery time left:          " << HMS(data.seconds_left_battery()+data.seconds_battery_correction()) << endl;

   if(show_seconds_left_battery_adaptive && !do_second_correction)
      cout << "Adapted battery time left:  " << HMS(data.seconds_left_battery_adaptive()) << endl;

   if(show_seconds_left_battery_adaptive && do_second_correction)
      cout << "Adapted battery time left:  " << HMS(data.seconds_left_battery_adaptive()+data.seconds_battery_correction_adaptive()) << endl;

   if(show_seconds_left_charge && !do_second_correction)
      cout << "Charge time left:           " << HMS(data.seconds_left_charge()) << endl;

   if(show_seconds_left_charge && do_second_correction)
      cout << "Charge time left:           " << HMS(data.seconds_left_charge()+data.seconds_charge_correction()) << endl;

   if(show_seconds_left_charge_adaptive && !do_second_correction)
      cout << "Adapted charge time left:   " << HMS(data.seconds_left_charge_adaptive()) << endl;

   if(show_seconds_left_charge_adaptive && do_second_correction)
      cout << "Adapted charge time left:   " << HMS(data.seconds_left_charge_adaptive()+data.seconds_charge_correction_adaptive()) << endl;

   if(show_seconds_battery_total)
      cout << "Total battery time:         " << HMS(data.seconds_battery_total()) << endl;

   if(show_seconds_battery_total_adaptive)
      cout << "Adapted total battery time: " << HMS(data.seconds_battery_total_adaptive()) << endl;
      
   if(show_seconds_charge_total)
      cout << "Total charge time:          " << HMS(data.seconds_charge_total()) << endl;

   if(show_seconds_charge_total_adaptive)
      cout << "Adapted total charge time:  " << HMS(data.seconds_charge_total_adaptive()) << endl;
      
   if(show_profile_logging)
   {
      if(data.profile_logging_setting())
      {
         cout << "Profile logging enabled." << endl;
         cout << "Current file: " << data.profile_filename(
                                       data.current_profile_number(),
                                       data.current_profile_type()) << endl;
      }
      else
         cout << "Profile logging disabled." << endl;
   }   
   if(show_credits)
   {
      cout << endl;
      cout << "Special thanks go to:" << endl << endl;
      cout << "Mohanty Mitrabhanu      for his scientific paper mentioning ibam"<< endl;
      cout << "Dan Egnor               for his sweetcode article" << endl;
      cout << "Martin Wuertele         for the debian port" << endl;
      cout << "Seth Golub              for code improvements" << endl;
      cout << "Misha Nasledov          for the gkrellm2-patch" << endl;
      cout << "Matthew Richardson      for the gentoo support" << endl;
      cout << "Florian Ragwitz         for the PMU support" << endl;
      cout << "Matthias Grimm          for the extended PMU support and pbbuttons.berlios.de" << endl;
      cout << "Peter Gaal              for testing and the APM bugfix" << endl;
      cout << "Brad Sawatzky           for the same APM bugfix" << endl;
   }
      
   return 0;
}

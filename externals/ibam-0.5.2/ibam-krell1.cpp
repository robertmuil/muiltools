/* demo2.c	- requires GKrellM 1.2.0 or better
|		gcc -fPIC `gtk-config --cflags` `imlib-config --cflags-gdk` -c demo2.c
|		gcc -shared -Wl -o demo2.so demo2.o
|		gkrellm -p demo2.so
*/

#include "ibam.hpp"

extern "C" {

#define private gkrell_private
#include <gkrellm/gkrellm.h>

  /* CONFIG_NAME would be the name in the configuration tree, but this demo
  |  does not have a config.  See demo1.c for that.
  */
#define	CONFIG_NAME	"Ibam"

  /* STYLE_NAME will be the theme subdirectory for custom images for this
  |  plugin and it will be the gkrellmrc style name for custom settings.
  */
#define	STYLE_NAME	"ibam"

  /* This demo just makes up some data for the krell to show.
  */
#define	KRELL_FULL_SCALE	30

static Monitor	*monitor;
static Panel	*panel;
static gint		style_id;
static Krell	*krell;
static Decal   *decal_text;

static void
update_plugin()
    {
	if (GK.second_tick)
		{
		   static ibam a;
		   static char buffer[80];
		   char *l;
		   static char *bat="batt";
		   static char *charge="chrg";
		   static char *full="full";
		   static long lasttime=time(NULL);
		   a.update();
		   if(a.valid())
		   {
		      int updateadd=0;
		      
		      if(time(NULL)<lasttime+20) 
   		      a.update_statistics();
   		   else
   		      a.ignore_statistics();
   		   
   		   lasttime=time(NULL);
   		   
		      a.save();
   		   gkrellm_update_krell(panel, krell, a.percent_battery()*KRELL_FULL_SCALE/100);
   		   int minutes;
   		   l=bat;
   		   if(a.onBattery())
   		      minutes=(a.seconds_left_battery_adaptive()
   		              +a.seconds_battery_correction()+30)/60;
   		   else if(a.charging())
   		   {
   		      minutes=(a.seconds_left_charge_adaptive()
   		              +a.seconds_charge_correction()+30)/60;
   		      l=charge;
   		      updateadd=10000;
   		   } else
   		   {
   		      minutes=a.seconds_left_battery()/60;
               l=full;
               updateadd=20000;
            }
            if(minutes<0)
               minutes=0;
   		   sprintf(buffer,"%s %2d:%02d",l,minutes/60,minutes%60);
   	      gkrellm_draw_decal_text(panel,decal_text,buffer,minutes+updateadd);


		   /* Updating a krell (or drawing a decal) draws only into local
		   |  pixmaps.  After all krells and decals are "drawn", they must be
		   |  really drawn to the screen with gkrellm_draw_panel_layers().
		   */
		      gkrellm_draw_panel_layers(panel);
		   } else
		   {
		      gkrellm_update_krell(panel, krell, 0);
		      gkrellm_draw_decal_text(panel,decal_text,"no data",99999);
		      gkrellm_draw_panel_layers(panel);
   		}   
		}
	}

static gint
panel_expose_event(GtkWidget *widget, GdkEventExpose *ev)
    {
    gdk_draw_pixmap(widget->window,
            widget->style->fg_gc[GTK_WIDGET_STATE (widget)],
            panel->pixmap, ev->area.x, ev->area.y, ev->area.x, ev->area.y,
            ev->area.width, ev->area.height);
    return FALSE;
	}

static void
create_plugin(GtkWidget *vbox, gint first_create)
	{
	Style			*style;
	TextStyle   *textstyle;
	GdkImlibImage	*krell_image;

	/* This create_plugin() routine is a create event routine which
	|  will be called when GKrellM is re-built at every theme or horizontal
	|  size change.  The idea is to allocate data structures and do some
	|  initialization only once (at first_create) and do decal and krell
	|  creation and plugin local image loading each time so theme changes
	|  will be picked up.
	|  Before this routine is called during the re-build, all of the krells
	|  and decals you previously created will have been destroyed.  However,
	|  for cases where a plugin wants to manage the decal and krell lists,
	|  it is possible to prevent the automatic krell and decal destruction.
	*/
	if (first_create)
		panel = gkrellm_panel_new0();

	/* Each plugin that has obtained a style_id (in init_plugin()) can use
	|  a default krell that may have been custom themed.  Additional custom
	|  krells may be created, but here we just use the default krell.  To
	|  create a kell, use our style (which has information about the krell
	|  depth, hot spot, and y offset into the panel), and our krell image.
	*/
	style = gkrellm_meter_style(style_id);
	krell_image = gkrellm_krell_meter_image(style_id);
	krell = gkrellm_create_krell(panel, krell_image, style);
	
	textstyle = gkrellm_meter_textstyle(style_id);
	
	decal_text = gkrellm_create_decal_text(panel, "IBAM", textstyle, style, -1, -1, -1);

	/* The default for GKrellM data update routines is to expect monotonically
	|  increasing data values.  So the real data values stored for display are
	|  differences between successive data updates.  But the data this demo
	|  krell will measure will be values within a fixed range, so we must
	|  turn off the monotonic mode.
	*/
	gkrellm_monotonic_krell_values(krell, FALSE);

	/* Set the kell full scale value and a krell scaling factor.  The scaling
	|  factor should almost always be 1.  Only chart styled krells that have
	|  a small full scale value might need a scaling factor greater than 1.
	*/
	gkrellm_set_krell_full_scale(krell, KRELL_FULL_SCALE, 1);

	/* Configuring a panel means to determine the height needed to accomodate
	|  its label and all of the created decals and krells that it contains.
	|  This is where we set the label on the panel to be "Plugin".  Many
	|  plugins will have panels with changing text or pixmap decals and will
	|  not use a label at all.  In those cases, just pass NULL for the label.
	|  Some plugins may want to have a fixed panel height.  Those should
	|  call gkrellm_panel_configure_add_height() instead of this:
	*/
	gkrellm_panel_configure(panel, NULL , style);

	/* Finally create the panel.  It will have a background image which will
	|  be the theme default or plugin specific if created by the theme maker.
	*/
	gkrellm_panel_create(vbox, monitor, panel);
	
	gkrellm_draw_decal_text(panel,decal_text,"IBAM",-1);

	if (first_create)
	    gtk_signal_connect(GTK_OBJECT (panel->drawing_area), "expose_event",
    	        (GtkSignalFunc) panel_expose_event, NULL);
	}


/* The monitor structure tells GKrellM how to call the plugin routines.
*/
static Monitor	plugin_mon	=
	{
	CONFIG_NAME,        /* Title for config clist.   */
	0,					/* Id,  0 if a plugin       */
	create_plugin,		/* The create function      */
	update_plugin,		/* The update function      */
	NULL,				/* The config tab create function   */
	NULL,				/* Apply the config function        */

	NULL,				/* Save user config			*/
	NULL,				/* Load user config			*/
	NULL,				/* config keyword			*/

	NULL,				/* Undefined 2	*/
	NULL,				/* Undefined 1	*/
	NULL,				/* private	*/

	MON_MAIL,			/* Insert plugin before this monitor			*/

	NULL,				/* Handle if a plugin, filled in by GKrellM     */
	NULL				/* path if a plugin, filled in by GKrellM       */
	};


  /* All GKrellM plugins must have one global routine named init_plugin()
  |  which returns a pointer to a filled in monitor structure.
  */
Monitor *
init_plugin()
	{
	/* If this next call is made, the background and krell images for this
	|  plugin can be custom themed by putting bg_meter.png or krell.png in the
	|  subdirectory STYLE_NAME of the theme directory.  Text colors (and
	|  other things) can also be specified for the plugin with gkrellmrc
	|  lines like:  StyleMeter  STYLE_NAME.textcolor orange black shadow
	|  If no custom theming has been done, then all above calls using
	|  style_id will be equivalent to style_id = DEFAULT_STYLE_ID.
	*/
	style_id = gkrellm_add_meter_style(&plugin_mon, STYLE_NAME);
	monitor = &plugin_mon;
	return &plugin_mon;
	}
}

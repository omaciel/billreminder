#!/usr/bin/env python
#-*- coding:utf-8 -*-

import pygtk
pygtk.require('2.0')
import gtk
import gobject
import pango
import datetime
from math import pi, floor
import warnings

debug = False

class Bullet(object):
    OVERDUE = int('001', 2)
    TO_BE_PAID = int('010', 2)
    PAID = int('100', 2)

    debug = False

    def __init__(self, date=None, amountDue=None, estimated=False, status=0,
      overthreshold=False, multi=False, tooltip=''):
        self.date = date
        self.amountDue = amountDue
        self.estimated = estimated
        self.status = status
        self.overthreshold = overthreshold
        self.multi = multi
        self.tooltip = tooltip
        if self.debug:
            print "Bullet created: ", self.date

class Timeline(gtk.DrawingArea):
    """ A widget that displays a timeline and allows the user to select a
    date interval
    """
    DAY, WEEK, MONTH, YEAR = range(4)
    DIVS = {
        DAY: 16,
        WEEK: 16,
        MONTH: 24,
        YEAR: 10
    }

    debug = False

    __gsignals__ = {
        'realize': 'override',
        'unrealize': 'override',
        'expose-event': 'override',
        'button-press-event': 'override',
        'button-release-event': 'override',
        'motion-notify-event': 'override',
        'key-press-event': 'override'
    }

    def __init__(self, date=None, callback=None):
        """ Timeline widget constructor

        Parameter:
            - date is a datetime.date object or a tuple (year, month, day).
              By default it is datetime.date.today()
            - callback is a functions that receive a datatetime.date object
              and return a Bullet object
        """

        # Treat the parameter
        if date and not isinstance(date, datetime.date) and \
          isinstance(date, tuple) and len(date) == 3:
            date = datetime.date(date[0], date[1], date[2])
        else:
            date = datetime.date.today()

        if callback:
            self._bullet_func = callback
        else:
            self._bullet_func = lambda date_, type_: None

        # Set defaults
        self._mindex = 0
        self._type = self.DAY
        self._display_days = self.DIVS[self._type]
        self._dates = {}
        self.start_date = None
        self.end_date = None
        self._bullets = {}
        self._box_rect = gtk.gdk.Rectangle()
        self._timer = None
        self._scroll_delay = 1800 / self._display_days
        self._pressed = False
        self._dragged = False
        self._clicked_position = -1
        self.value = date
        self.orientation = gtk.ORIENTATION_HORIZONTAL
        self._position = round((self._display_days - 1) / 2)

        # Widget initialization
        self.drag = False
        super(gtk.DrawingArea, self).__init__()
        self.add_events(
            gtk.gdk.BUTTON_MOTION_MASK |
            gtk.gdk.BUTTON_PRESS_MASK |
            gtk.gdk.BUTTON_RELEASE_MASK |
            gtk.gdk.SCROLL_MASK
        )
        gobject.signal_new(
            'value-changed',
            Timeline,
            gobject.SIGNAL_RUN_LAST,
            gobject.TYPE_NONE,
            (gobject.TYPE_PYOBJECT,)
        )
        gobject.signal_new(
            'scroll',
            Timeline,
            gobject.SIGNAL_RUN_LAST,
            gobject.TYPE_NONE,
            (gobject.TYPE_PYOBJECT,)
        )
        self. connect('size-allocate', self.on_size_allocate)

    def do_realize(self):
        self.set_flags(self.flags() | gtk.REALIZED)
        events = (
            gtk.gdk.EXPOSURE_MASK |
            gtk.gdk.BUTTON_PRESS_MASK |
            gtk.gdk.POINTER_MOTION_MASK |
            gtk.gdk.KEY_PRESS_MASK |
            gtk.gdk.KEY_RELEASE_MASK
        )
        self.window = gtk.gdk.Window(
            self.get_parent_window(),
            x=self.allocation.x,
            y=self.allocation.y,
            width=self.allocation.width,
            height=self.allocation.height,
            window_type=gtk.gdk.WINDOW_CHILD,
            wclass=gtk.gdk.INPUT_OUTPUT,
            visual=self.get_visual(),
            colormap=self.get_colormap(),
            event_mask=self.get_events() | events
        )
        self.window.set_user_data(self)
        self.style.attach(self.window)
        self.style.set_background(self.window, gtk.STATE_NORMAL)
        self.set_property('can-focus', True)

        self.select_date(self.value.day, self.value.month, self.value.year)

        # Define widget minimum size
        self.set_size_request(540, 81)

    def do_unrealize(self):
        self.window.destroy()

    def do_expose_event(self, event):
        self.draw()
        return False

    def refresh(self):
        self._bullets = {}
        self._dist_dates()
        self.queue_draw_area(
            0, 0, self.allocation.width, self.allocation.height
        )

    def draw(self, redraw=False):
        if self.orientation == gtk.ORIENTATION_HORIZONTAL:
            self._hdraw(redraw)
        elif self.orientation == gtk.ORIENTATION_VERTICAL:
            raise NotImplementedError, \
              'self.orientation == gtk.ORIENTATION_VERTICAL'
        else:
            raise ValueError, 'self.orientation'

    def _hdraw(self, redraw=False):
        """ Draw a horizontal timeline """
        self._layout = self.create_pango_layout('')
        cr = self.window.cairo_create()

        # Draw the base box
        self.window.draw_rectangle(
            self.style.base_gc[gtk.STATE_NORMAL], True,
            self._box_rect.x,
            self._box_rect.y,
            self._box_rect.width,
            self._box_rect.height
        )

        self.style.paint_shadow(
            self.window, self.state,
            gtk.SHADOW_IN, None, self, '',
            self._box_rect.x, self._box_rect.y,
            self._box_rect.width + 1,
            self._box_rect.height
        )

        y_ = self._box_rect.y + self._box_rect.height / 2
        
        line_cg = self.style.text_gc
        fg_color = {
            'red': self.parent.style.text[gtk.STATE_NORMAL].red / 65535.0,
            'green': self.parent.style.text[gtk.STATE_NORMAL].green / 65535.0,
            'blue': self.parent.style.text[gtk.STATE_NORMAL].blue / 65535.0
        }
        radius = self._bullet_radius
        radius_by_two = radius / 2
        radius_by_three = radius / 3
        radius_by_four = radius / 4
        radius_by_five = radius / 5
        radius_by_seven = radius / 7
        radius_by_eight = radius / 8
        two_pi = 2 * pi;
        arc = (two_pi) / 40
        y = int(y_)
            
        # Go through all visible positions
        for i in range(self._display_days):
            line_h = 3
            x = self._box_rect.x + self._div_width * i + self._div_width / 2

            # Draw bullets
            if self._bullets[i] and i < self._display_days:
                bullet_ = self._bullets[i]

                # Draw the behind bullet when is multiple
                if bullet_.multi:
                    if bullet_.status & Bullet.TO_BE_PAID:
                        cr.set_source_rgba(0.13, 0.4, 0.48)
                    if bullet_.status & Bullet.OVERDUE:
                        cr.set_source_rgba(0.47, 0, 0)
                    if bullet_.status & Bullet.PAID:
                        cr.set_source_rgba(0.19, 0.51, 0)
                    ## Move to the position of behind bullet
                    x += radius_by_four
                    y += radius_by_three
                    ## Draw it
                    cr.arc(x, y, radius, 0, two_pi)
                    cr.fill_preserve()
                    cr.set_line_width(radius_by_eight)
                    cr.stroke()
                    ## Move back to the main bullet position
                    x -= radius_by_four
                    y -= radius_by_three

                # Draw the main bullet body
                ## Set the color 
                if bullet_.status & Bullet.PAID:
                    cr.set_source_rgb(0.27, 0.81, 0.44)
                if bullet_.status & Bullet.OVERDUE:
                    cr.set_source_rgb(1, 0.16, 0.16)
                if bullet_.status & Bullet.TO_BE_PAID:
                    cr.set_source_rgb(0.52, 0.81, 0.87)
                ## Draw it
                cr.arc(x, y, radius, 0, two_pi)
                cr.fill()

                # Draw the main bullet border
                ## Set the color 
                if bullet_.status & Bullet.PAID:
                    cr.set_source_rgb(0.19, 0.51, 0)
                if bullet_.status & Bullet.OVERDUE:
                    cr.set_source_rgb(0.47, 0, 0)
                if bullet_.status & Bullet.TO_BE_PAID:
                    cr.set_source_rgb(0.13, 0.4, 0.48)

                # Set different border size if is overthreshold
                if bullet_.overthreshold:
                    cr.set_line_width(radius_by_three)
                else:
                    cr.set_line_width(radius_by_five)

                # Draw dotted border if is estimeded
                if bullet_.estimated:
                    for j in range(0, 40, 2):
                        if bullet_.overthreshold:
                            cr.arc(x, y, radius, arc * j, arc * (j + 1))
                        else:
                            cr.arc(x, y, radius, arc * j, arc * (j + 0.5))
                        cr.stroke()
                # Else draw the solid border
                else:
                    cr.arc(x, y, radius, 0, two_pi)
                    cr.stroke()

            # Draw vertical dashed line if the position is for today
            if self._dates[i] == datetime.date.today():
                cr.set_source_rgba(
                    fg_color['red'], fg_color['green'], fg_color['blue'], 0.75
                )
                cr.set_line_width(max(radius_by_eight, 0.8))
                cr.set_source_rgb(0.4, 0.4, 0.4)
                h_ = (self._box_rect.height + self._box_rect.y) / 10
                for j in range(0, 10, 2):
                    cr.move_to(x, self._box_rect.y + h_ * j + 1)
                    cr.line_to(x, self._box_rect.y + h_ * (j + 1))
                    cr.stroke()

            # Draw dots
            cr.set_source_rgba(
                fg_color['red'], fg_color['green'], fg_color['blue'], 0.75
            )
            if self._dates[i].weekday() == 6:
                cr.arc(x, y, radius_by_five, 0, two_pi)
            else:
                cr.arc(x, y, radius_by_seven, 0, two_pi)
            cr.fill()

            #Draw label
            ## Draw the year label
            if (self._dates[i].day, self._dates[i].month) == (1, 1) or \
              (self._dates[i].month == 1 and self._dates[i].day <= 7 and
              self._type == self.WEEK):
                if i < self._display_days:
                    self._layout.set_markup(
                        '<small>' + str(self._dates[i].year) + '</small>'
                    )
                    size_ = self._layout.get_pixel_size()
                    self.style.paint_layout(
                        self.window, self.state, False,
                        None, self, '',
                        int(self._box_rect.x + \
                        self._div_width * i + \
                        self._div_width / 2 - size_[0] / 2),
                        self._box_rect.y + \
                        self._box_rect.height + 12,
                        self._layout
                    )

                line_h = 6

            ## Draw the month label
            elif ((self._dates[i].day == 1 and self._type == self.DAY) or \
              (self._dates[i].day <= 7 and self._type == self.WEEK) or \
              (i == 0 and self.start_date.month == self.end_date.month)):
                if i < self._display_days:
                    self._layout.set_markup(
                        '<small>' + self._dates[i].strftime('%b') + '</small>'
                    )
                    size_ = self._layout.get_pixel_size()
                    self.style.paint_layout(
                        self.window, self.state, False,
                        None, self, '',
                        int(self._box_rect.x + \
                        self._div_width * i + \
                        self._div_width / 2 - size_[0] / 2),
                        self._box_rect.y + \
                        self._box_rect.height + 12,
                        self._layout
                    )

                line_h = 6

            self.window.draw_rectangle(
                line_cg[self.state],
                True,
                int(self._box_rect.x + self._div_width * i +
                self._div_width / 2),
                self._box_rect.height + \
                self._box_rect.y - 2,
                1, line_h
            )

            ## Draw day label
            if i < self._display_days and \
              (self.display_days < 20 or self._dates[i].weekday() == 0 or \
              self._dates[i] == self.value):
                # Draw today with bold font
                if self._dates[i] == datetime.date.today():
                    self._layout.set_markup(
                        '<b><small>' + str(self._dates[i].day) + '</small></b>'
                    )
                else:
                    self._layout.set_markup(
                        '<small>' + str(self._dates[i].day) + '</small>'
                    )
                state_ = self.state
                size_ = self._layout.get_pixel_size()
                if self._dates[i] == self.value:
                    state_ = gtk.STATE_SELECTED
                    self.window.draw_rectangle(
                        self.style.base_gc[gtk.STATE_SELECTED],
                        True,
                        int(self._box_rect.x + self._div_width * i),
                        int(self._box_rect.y + self._box_rect.height),
                        int(self._div_width + 1),
                        size_[1]
                    )
                self.style.paint_layout(
                    self.window, state_, False,
                    None, self, '',
                    int(self._box_rect.x + \
                    self._div_width * i + \
                    self._div_width / 2 - size_[0] / 2),
                    self._box_rect.y + \
                    self._box_rect.height,
                    self._layout
                )

        # Draw the central line
        cr.set_line_width(max(radius_by_eight, 0.5))
        cr.set_source_rgba(
            fg_color['red'], fg_color['green'], fg_color['blue'], 0.5
        )
        cr.move_to(self._box_rect.x + 1, y)
        cr.line_to(self._box_rect.width + self._box_rect.x, y)
        cr.stroke()

        mx, my = self.get_pointer()

        # Draw the Arrows
        arrow_y = self._box_rect.y + self._box_rect.height / 2 - 5
        ## Draw the left arrow
        self.style.paint_arrow(
            self.window, self.state, gtk.SHADOW_IN,
            None, self, '', gtk.ARROW_LEFT, True,
            self._box_rect.x - 15, arrow_y,
            8, 10
        )

        ## Draw the right arrow
        self.style.paint_arrow(
            self.window, self.state, gtk.SHADOW_IN,
            None, self, '', gtk.ARROW_RIGHT, True,
            self._box_rect.x + self._box_rect.width + 9, arrow_y,
            8, 10
        )

        # Draw the focus rect
        if self.get_property('has-focus'):
            self.style.paint_focus(
                self.window, self.state, None, self, '',
                1, 1,
                self.width - 2, self.height -2
            )


    def do_key_press_event(self, event):
        if gtk.gdk.keyval_name(event.keyval) == 'Right':
            # Control+right - go to next month
            if event.state & gtk.gdk.CONTROL_MASK:
                month = (self.value.month % 12) + 1
                year = self.value.year + (self.value.month) / 12
                self.select_month(month=month, year=year)
            # Right - scroll right
            else:
                self.scroll(gtk.gdk.SCROLL_RIGHT)
                
        if gtk.gdk.keyval_name(event.keyval) ==  'Left':
            # Control+left - go to prev month
            if event.state & gtk.gdk.CONTROL_MASK:
                year = self.value.year - int(not self.value.month - 1)
                month = self.value.month - 1 + (self.value.year - year) * 12
                self.select_month(month=month, year=year)
            # Left - scroll left
            else:
                self.scroll(gtk.gdk.SCROLL_LEFT)
        
        # "+" - zoom in
        if gtk.gdk.keyval_name(event.keyval) == 'plus' \
          or gtk.gdk.keyval_name(event.keyval) == 'KP_Add':
            self.display_days -= 2
        # "-" - zoom out
        if gtk.gdk.keyval_name(event.keyval) == 'minus' or \
          gtk.gdk.keyval_name(event.keyval) == 'KP_Subtract':
            self.display_days += 2
        # Home - go to Today
        if gtk.gdk.keyval_name(event.keyval) == 'Home':
            self.value = datetime.date.today()
            self._value_changed()
        # PageUp
        if gtk.gdk.keyval_name(event.keyval) == 'Page_Up':
            self.set_position(self._position - self.display_days)
            self.move(self._box_rect.width / 2)
        # PageDow 
        if gtk.gdk.keyval_name(event.keyval) == 'Page_Down':
            self.set_position(self._position + self.display_days)
            self.move(self._box_rect.width / 2)
        self.queue_draw_area(
            0, 0, self.allocation.width, self.allocation.height
        )
        
        if self.debug:
            print gtk.gdk.keyval_name(event.keyval)

    def do_button_release_event(self, event):
        # Get the mouse position and set focus to the wiget
        mx, my = self.get_pointer()
        self.drag = False
        
        # Released the click with the mouse left buttom
        if event.button == 1:
            self._pressed = False
            # Stop the autoscroll trigger timer
            if self._timer:
                gobject.source_remove(self._timer)
                self._timer = None
            # Released from the main box area
            if mx > self._box_rect.x and \
              mx < self._box_rect.width + self._box_rect.x:
                # The user didn't dragged the timeline
                if not self._dragged:
                    self.move(mx - self._div_width / 2)
                    gobject.timeout_add(
                        self._scroll_delay, self._center_selection
                    )
                if mx < self._box_rect.x or \
                  mx > self._box_rect.x + self._box_rect.width or \
                  my > self._box_rect.y + self._box_rect.height:
                    self.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.HAND2))
                else:
                    self.window.set_cursor(None)
            self.queue_draw_area(0, 0, self.allocation.width,
                                 self.allocation.height)
        if self._dragged:
            self.move(self._box_rect.width / 2)
            self._dragged = False
            self._pressed = False
        return False

    def do_button_press_event(self, event):
        # Get the mouse position and set focus to the wiget
        mx, my = self.get_pointer()
        self.grab_focus()

        # Stop the autoscroll trigger timer
        if self._timer:
            gobject.source_remove(self._timer)
            self._timer = None
        
        # Clicked with the mouse left buttom
        if event.button == 1:
            # Clicked on the left arrow
            if mx < self._box_rect.x:
                self.scroll(gtk.gdk.SCROLL_LEFT)
                # Start the autoscroll trigger timer
                self._timer = gobject.timeout_add(
                    500, self.auto_scroll, gtk.gdk.SCROLL_LEFT
                )
            # Clicked on the right arrow
            elif mx > self._box_rect.width + self._box_rect.x:
                self.scroll(gtk.gdk.SCROLL_RIGHT)
                # Start the autoscroll trigger timer
                self._timer = gobject.timeout_add(
                    500, self.auto_scroll, gtk.gdk.SCROLL_RIGHT
                )
            # Clicked on the main box area
            elif mx > self._box_rect.x and \
              mx < self._box_rect.width + self._box_rect.x:
                self._pressed = True
                self._clicked_position = self._get_mouse_position()
        return False

    def do_motion_notify_event(self, event):
        mx, my = self.get_pointer()
        if self._pressed:
            self.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.HAND1))
            pos_ = self._get_mouse_position()
            if pos_ != self._clicked_position or self._dragged:
                self._dragged = True
                self.set_position(
                    (self.display_days / 2) + (pos_ - self._clicked_position), 
                    True
                )
            else:
                self._dragged = False
        else:
            # TODO Improve tooltip
            if mx < self._box_rect.x or \
              mx > self._box_rect.x + self._box_rect.width or \
              my > self._box_rect.y + self._box_rect.height:
                self.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.HAND2))
            elif my > self._box_rect.y - self._bullet_radius / 3 + \
              (self._box_rect.height - self._bullet_radius) / 2 and \
              my < self._box_rect.y + self._bullet_radius / 3  + \
              (self._box_rect.height / 2) + self._bullet_radius:
                if self._mindex != int(
                  (mx - self._box_rect.x) / self._div_width
                ):
                    self._mindex = int(
                        (mx - self._box_rect.x) / self._div_width
                    )
                    if self._mindex > -1 and \
                      self._mindex < self.DIVS[self._type] and \
                      self._bullets[self._mindex]:
                        gobject.timeout_add(
                            100, 
                            self.set_tooltip, 
                            self._bullets[self._mindex].tooltip
                        )
                    else:
                        self.set_tooltip_text(None)
                self.window.set_cursor(None)
            else:
                self._mindex = -1
                self.set_tooltip_text(None)
                self.window.set_cursor(None)
        #gobject.timeout_add(100, self.set_tooltip, str(mx))
        return False

    def do_scroll_event(self, event):
        # SCROLL_DOWN is used to be possible scroll using simple mousewheel
        if event.direction in (gtk.gdk.SCROLL_DOWN, gtk.gdk.SCROLL_RIGHT):
            self.scroll(gtk.gdk.SCROLL_RIGHT)
        else:
            self.scroll(gtk.gdk.SCROLL_LEFT)

    def set_tooltip(self, text=None):
        self.set_tooltip_text(text)
        return False

    def _get_mouse_position(self):
        mx, my = self.get_pointer()
        pos_  = (mx - self._div_width / 2 - self._box_rect.x) / self._div_width
        x = pos_ * self._div_width + self._box_rect.x
        if mx - self._div_width / 2 > x + self._div_width / 2:
            pos_ += 1
        return round(pos_)

    def _value_changed(self):
        self.day = self.value.day
        self.month = self.value.month
        self.year = self.value.year
        self._dist_dates()
        self.start_date = self._dates[0]
        self.end_date = self._dates[self._display_days - 1]
        self.emit('value-changed', self.value)
        if self.debug:
            print "Timeline.value: ", str(self.value)
            print "Timeline.start_date: ", self.start_date
            print "Timeline.end_date: ", self.end_date

    def on_size_allocate(self, widget, allocation):
        self.width = allocation.width
        self.height = allocation.height
        # Set timeline subdivisions size
        self._div_width = float(allocation.width - self._box_rect.x * 2) / \
                          self._display_days
        # Set Timeline box size
        self._box_rect.x = 21
        self._box_rect.y = 6
        self._box_rect.width = allocation.width - self._box_rect.x * 2
        self._box_rect.height = allocation.height - 33
        if self._box_rect.height < 0:
            self._box_rect.height = 0
        # Set Bullet radius
        if self._div_width - self._div_width / 4 > self._box_rect.height / 2:
            self._bullet_radius = (self._box_rect.height / 2) / 2
        else:
            self._bullet_radius = (self._div_width - self._div_width / 4) / 2

        return False

    def _dist_dates(self, first=None):
        """ Calculate dates for visible positions """
        if not first:
            # Define the first day if not provided
            selected = self.value
            if self._type == self.WEEK and selected.weekday() != 0:
                selected -= datetime.timedelta(days=selected.weekday())
            if self._type == self.DAY:
                first = selected - datetime.timedelta(days=self._position)
            elif self._type == self.WEEK:
                first = selected - datetime.timedelta(days=self._position * 7)
            elif self._type == self.MONTH:
                month = (selected.month - self._position) % 12
                year = selected.year + (selected.month - self._position) // 12
                if not month:
                    month = 12
                    year -= 1
                first = selected.replace(month=month, year=year)
            elif self._type == self.YEAR:
                first = selected.replace(year=selected.year - self._position)

        # Define the day and create the bullet object for each visible position
        if self._type == self.DAY:
            for i in range(self._display_days + 1):
                self._dates[i] = first + datetime.timedelta(days=i)
                self._bullets[i] = self._bullet_func(self._dates[i], self._type)
        elif self._type == self.WEEK:
            for i in range(self._display_days + 1):
                self._dates[i] = first + datetime.timedelta(days=i * 7)
                self._bullets[i] = self._bullet_func(self._dates[i], self._type)
        elif self._type == self.MONTH:
            for i in range(self._display_days + 1):
                month = (first.month + i) % 12
                year = first.year + (first.month + i) // 12
                if not month:
                    month = 12
                    year -= 1
                self._dates[i] = first.replace(day=1, month=month, year=year)
                self._bullets[i] = self._bullet_func(self._dates[i], self._type)
        elif self._type == self.YEAR:
            for i in range(self._display_days + 1):
                self._dates[i] = first.replace(
                    day=1, month=1, year=first.year + i
                )
                self._bullets[i] = self._bullet_func(self._dates[i], self._type)

    def scroll(self, direction, redraw=True):
        """ Scroll the timeline widget

            Parameters:
                - direction: gtk.gdk.SCROLL_LEFT or gtk.gdk.SCROLL_RIGHT
                - redraw: use False when scroll by dragging slider.
                  By default it is True.

            Return:
                Return True to be used in gobject.timeout_add()
        """
        if direction == gtk.gdk.SCROLL_LEFT:
            self.set_position(self._position + 1, redraw)
            self.emit('scroll', direction)
        elif direction == gtk.gdk.SCROLL_RIGHT:
            self.set_position(self._position - 1, redraw)
            self.emit('scroll', direction)
        else:
            raise ValueError, direction
        self.move(self._box_rect.width / 2)
        return True

    def auto_scroll(self, direction, redraw=True):
        """ Auto scroll the widget

            Parameters:
                - direction: gtk.gdk.SCROLL_LEFT or gtk.gdk.SCROLL_RIGHT
                - redraw: use False when scroll by dragging slider.
                  By default it is True.

            Return:
                Return False to run only one time when used in
                gobject.timeout_add()
        """
        self._timer = gobject.timeout_add(
            self._scroll_delay, self.scroll, direction, redraw
        )
        return False

    def _center_selection(self):
        if self._position > (self._display_days - 1) / 2:
            self.set_position(self._position - 1, True)
        elif self._position < (self._display_days - 1) / 2:
            self.set_position(self._position + 1, True)

        if self._position == (self._display_days - 1) / 2:
            self.value = self._dates[self._position]
            self._dist_dates()
            self._value_changed()

        return self._position != (self._display_days - 1) / 2

    def move(self, pos, update=True, redraw=True):
        position_old = self._position
        self._position = round((pos - self._box_rect.x) / self._div_width)
        x = self._position * self._div_width + self._box_rect.x
        if pos > x + self._div_width / 2:
            self._position += 1
            x += self._div_width
        self.queue_draw_area(
            0, 0, self.allocation.width, self.allocation.height
        )
        if self.debug :
            if not self._dragged:
                print "Timeline.position: ", self._position

        if update:
            # Update self.value
            if self._position < 0 or self._position > self._display_days - 1:
                return
            self.value = self._dates[self._position]
            self._dist_dates()
            self._value_changed()
        return position_old, self._position

    def get_position(self):
        return int(self._position)
        
    def set_position(self, pos, redraw=True):
        self._position = round(pos)
        x = pos * self._div_width + self._box_rect.x
        self.move(x, False, redraw)
        self._dist_dates()
        return int(self._position)

    position = property(get_position, set_position)

    def get_start_date(self):
        return self.start_date

    def get_end_date(self):
        return self.end_date

    def get_display_days(self):
        return self._display_days

    def set_display_days(self, days):
        days_old = self._display_days
        if days < 7:
            days = 7
            warnings.warn('Using the minimum allowed value: 7', RuntimeWarning)
        elif days > 61:
            days = 61
            warnings.warn('Using the maximum allowed value: 61', RuntimeWarning)
        if days == days_old:
            return
        self._display_days = days
        self._dist_dates()
        # Set timeline subdivisions size
        self.on_size_allocate(self, self.allocation)
        self._center_selection()
        self.queue_draw_area(
            0, 0, self.allocation.width, self.allocation.height
        )
    display_days = property(get_display_days, set_display_days)

    def get_type(self):
        """ Return timeline type
            (Timeline.DAY, Timeline.WEEK, Timeline.MONTH or Timeline.YEAR)
        """
        return self._type

    def set_type(self, display_type):
        if display_type not in (DAY, WEEK, MONTH, YEAR):
            raise ValueError
        self._type = display_type
        self._display_days = self.DIVS[self._type]
        self._dist_dates()
        self.queue_draw_area(
            0, 0, self.allocation.width, self.allocation.height
        )

    def get_interval(self):
        return self._interval

    def select_month(self, month=None, year=None):
        if month and not year and not self._type == self.YEAR:
            self.value = self.value.replace(month=month)
            self.set_position((self._display_days - 1) / 2)
            self._value_changed()
        if not month and year:
            self.value = self.value.replace(year=year)
            self.set_position((self._display_days - 1) / 2)
            self._value_changed()
        if month and year:
            self.value = self.value.replace(month=month, year=year)
            self.set_position((self._display_days - 1) / 2)
            self._value_changed()

    def select_day(self, day):
        if self._type in (self.DAY, self.WEEK):
            self.value = self.value.replace(day=day)
            self.set_position((self._display_days - 1) / 2)
            self._value_changed()

    def select_date(self, day, month, year):
        self.value = self.value.replace(day=day, month=month, year=year)
        self.queue_draw_area(0, 0, self.width, self.height)
        self._value_changed()

    def set_bullet_function(self, func):
        """
            Set the function to be used to create the bullet object for 
            a given date.
        """
        self._bullet_func = func

def bullet_cb(date, display_type):
    #print date, display_type

    bullets = []

    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    tomorrow = today + datetime.timedelta(days=1)

    # date=None, amountDue=None, estimated=False, status=0,
    # overthreshold=False, multi=False, tooltip=''
    if date == today - datetime.timedelta(days=3):
        return Bullet(date, 200, False, Bullet.PAID, False, True, 'PAID')
    elif date == today - datetime.timedelta(days=2):
        return Bullet(date, 200, False, Bullet.OVERDUE, False, True, 'OVERDUE')
    elif date == today - datetime.timedelta(days=1):
        return Bullet(date, 200, False, Bullet.OVERDUE | Bullet.PAID, False, True, 'OVERDUE and PAID')
    elif date == today:
        return Bullet(date, 50, False, Bullet.TO_BE_PAID, False, True, 'TO_BE_PAID')
    elif date == today + datetime.timedelta(days=1):
        return Bullet(date, 20, False, Bullet.TO_BE_PAID | Bullet.PAID, False, True, 'TO_BE_PAID and PAID')


    return None



if __name__ == '__main__':
    window = gtk.Window()
    window.set_title('Timeline')
    window.set_default_size(500, 70)
    timeline = Timeline(None, bullet_cb)
    timeline.debug = True
    timeline.display_days = 15
    window.add(timeline)
    window.connect('delete-event', gtk.main_quit)
    window.show_all()
    gtk.main()

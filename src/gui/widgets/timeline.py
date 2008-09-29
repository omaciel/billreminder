#!/usr/bin/env python
#-*- coding:utf-8 -*-

import pygtk
pygtk.require('2.0')
import gtk
import gobject
import pango
import datetime
from math import pi, floor

debug = False

class Bullet(object):
    OVERDUE, TO_BE_PAID, PAID = range(-1, 2)

    debug = False
    
    def __init__(self, date=None, amount=None, estimated=False, status=0,
      overthreshold=False, multi=False, tooltip=''):
        self.date = date
        self.amount = amount
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
    DIVS = {}
    DIVS[DAY] = 16
    DIVS[WEEK] = 16
    DIVS[MONTH] = 24
    DIVS[YEAR] = 10

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
            self._bullet_func = lambda date_: None

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
        self.position = round((self._display_days - 1) / 2)

        # Widget initialization
        self.drag = False
        super(gtk.DrawingArea, self).__init__()
        self.add_events(gtk.gdk.BUTTON_MOTION_MASK |
                        gtk.gdk.BUTTON_PRESS_MASK |
                        gtk.gdk.BUTTON_RELEASE_MASK |
                        gtk.gdk.SCROLL_MASK)
        gobject.signal_new('value-changed',
                           Timeline,
                           gobject.SIGNAL_RUN_LAST,
                           gobject.TYPE_NONE,
                           (gobject.TYPE_PYOBJECT,))
        gobject.signal_new('scroll',
                           Timeline,
                           gobject.SIGNAL_RUN_LAST,
                           gobject.TYPE_NONE,
                           (gobject.TYPE_PYOBJECT,))
        self. connect('size-allocate', self.on_size_allocate)

    def do_realize(self):
        self.set_flags(self.flags() | gtk.REALIZED)
        events = (gtk.gdk.EXPOSURE_MASK |
                  gtk.gdk.BUTTON_PRESS_MASK |
                  gtk.gdk.POINTER_MOTION_MASK |
                  gtk.gdk.KEY_PRESS_MASK |
                  gtk.gdk.KEY_RELEASE_MASK)
        self.window = gtk.gdk.Window(self.get_parent_window(),
                                     x=self.allocation.x,
                                     y=self.allocation.y,
                                     width=self.allocation.width,
                                     height=self.allocation.height,
                                     window_type=gtk.gdk.WINDOW_CHILD,
                                     wclass=gtk.gdk.INPUT_OUTPUT,
                                     visual=self.get_visual(),
                                     colormap=self.get_colormap(),
                                     event_mask=self.get_events() | events)
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

    def draw(self, redraw=False):
        if self.orientation == gtk.ORIENTATION_HORIZONTAL:
            self._hdraw(redraw)
        elif self.orientation == gtk.ORIENTATION_VERTICAL:
            raise NotImplementedError, \
              'self.orientation == gtk.ORIENTATION_VERTICAL'
        else:
            raise ValueError, 'self.orientation'

    def _hdraw(self, redraw=False):
        # TODO Organize
        """ Draw a horizontal timeline """
        self._layout = self.create_pango_layout('')
        
        # base box
        self.window.draw_rectangle(self.style.base_gc[gtk.STATE_NORMAL], True,
                                   self._box_rect.x,
                                   self._box_rect.y,
                                   self._box_rect.width,
                                   self._box_rect.height)

        cr = self.window.cairo_create()

        self.style.paint_shadow(self.window, self.state,
                                gtk.SHADOW_IN, None, self, '',
                                self._box_rect.x, self._box_rect.y,
                                self._box_rect.width + 1,
                                self._box_rect.height)

        y_ = self._box_rect.y + self._box_rect.height / 2
        ## lines and bullets
        y = int(self._box_rect.y + self._box_rect.height / 2)
        for i in range(self._display_days):
            line_h = 3
            line_cg = self.style.dark_gc

            x = self._box_rect.x + self._div_width * i + self._div_width / 2
            width = self._bullet_radius
            
            # bullets
            if self._bullets[i] and i < self._display_days:
                arc = (2 * pi) / 40
                bullet_ = self._bullets[i]
                if bullet_.status == Bullet.PAID:
                    cr.set_source_rgb(0.27, 0.81, 0.44)
                    cr.set_source_rgb(0.19, 0.51, 0)
                elif bullet_.status == Bullet.OVERDUE:
                    cr.set_source_rgb(1, 0.16, 0.16)
                else:
                    cr.set_source_rgb(0.52, 0.81, 0.87)
                if bullet_.multi:
                    x += width / 4
                    y += width / 3
                    cr.arc(x, y, width, 0, 2 * pi)
                    cr.fill_preserve()
                    cr.set_line_width(width / 8)
                    if bullet_.status == Bullet.PAID:
                        cr.set_source_rgb(0.19, 0.51, 0)
                    elif bullet_.status == Bullet.OVERDUE:
                        cr.set_source_rgb(0.47, 0, 0)
                    else:
                        cr.set_source_rgb(0.13, 0.4, 0.48)
                    #cr.arc(x, y, width, 0, 2 * pi)
                    cr.stroke()
                    x -= width / 4
                    y -= width / 3
                if bullet_.status == Bullet.PAID:
                    cr.set_source_rgb(0.27, 0.81, 0.44)
                elif bullet_.status == Bullet.OVERDUE:
                    cr.set_source_rgb(1, 0.16, 0.16)
                else:
                    cr.set_source_rgb(0.52, 0.81, 0.87)
                cr.arc(x, y, width, 0, 2 * pi)
                cr.fill()

                if bullet_.status == Bullet.PAID:
                    cr.set_source_rgb(0.19, 0.51, 0)
                elif bullet_.status == Bullet.OVERDUE:
                    cr.set_source_rgb(0.47, 0, 0)
                else:
                    cr.set_source_rgb(0.13, 0.4, 0.48)

                if bullet_.overthreshold:
                    cr.set_line_width(width / 3)
                else:
                    cr.set_line_width(width / 5)
                if bullet_.estimated:
                    for j in range(0, 40, 2):
                        if bullet_.overthreshold:
                            cr.arc(x, y, width, arc * j, arc * (j + 1))
                        else:
                            cr.arc(x, y, width, arc * j, arc * (j + 0.5))
                        cr.stroke()
                else:
                    cr.arc(x, y, width, 0, 2 * pi)
                    cr.stroke()

            y = y_

            cr.set_source_rgb(0.4, 0.4, 0.4)
            cr.arc(x, y, width / 5, 0, 2 * pi)
            cr.fill()
            if self._dates[i].weekday() == 0:
                cr.set_line_width(max(width / 8, 0.8))
                cr.move_to(x, y - max(width / 2, 4))
                cr.line_to(x, y + max(width / 2, 4))
                cr.stroke()

            if self._dates[i] == datetime.date.today():
                cr.set_line_width(max(width / 8, 0.8))
                cr.set_source_rgb(0.4, 0.4, 0.4)
                h_ = (self._box_rect.height + self._box_rect.y) / 10
                for j in range(0, 10, 2):
                    cr.move_to(x, self._box_rect.y + h_ * j + 1)
                    cr.line_to(x, self._box_rect.y + h_ * (j + 1))
                    cr.stroke()

            ## year label
            if (self._dates[i].day, self._dates[i].month) == (1, 1) or \
              (self._dates[i].month == 1 and self._dates[i].day <= 7 and
              self._type == self.WEEK):
                if i < self._display_days:
                    self._layout.set_markup('<small>' + str(self._dates[i].year) + '</small>')
                    size_ = self._layout.get_pixel_size()
                    self.style.paint_layout(self.window, self.state, False,
                                            None, self, '',
                                            int(self._box_rect.x + \
                                            self._div_width * i + \
                                            self._div_width / 2 - size_[0] / 2),
                                            self._box_rect.y + \
                                            self._box_rect.height + 10,
                                            self._layout)
                                            
                line_h = 6

            ## month label
            elif ((self._dates[i].day == 1 and self._type == self.DAY) or \
              (self._dates[i].day <= 7 and self._type == self.WEEK) or \
              (i == 0 and self.start_date.month == self.end_date.month)):
                if i < self._display_days:
                    self._layout.set_markup('<small>' + self._dates[i].strftime('%b') + '</small>')
                    size_ = self._layout.get_pixel_size()
                    self.style.paint_layout(self.window, self.state, False,
                                            None, self, '',
                                            int(self._box_rect.x + \
                                            self._div_width * i + \
                                            self._div_width / 2 - size_[0] / 2),
                                            self._box_rect.y + \
                                            self._box_rect.height + 10,
                                            self._layout)
                                            
                line_h = 6

            self.window.draw_rectangle(line_cg[self.state],
                                       True,
                                       int(self._box_rect.x + self._div_width * i +
                                       self._div_width / 2),
                                       self._box_rect.height + \
                                       self._box_rect.y - 2,
                                       1, line_h)

            ## day label
            # Draw today with bold font
            if i < self._display_days and \
              (self.display_days < 20 or self._dates[i].weekday() == 0 or \
              self._dates[i] == self.value):
                if self._dates[i] == datetime.date.today():
                    self._layout.set_markup('<b><small>' + str(self._dates[i].day) + '</small></b>')
                else:
                    self._layout.set_markup('<small>' + str(self._dates[i].day) + '</small>')
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
                        size_[1])
                self.style.paint_layout(self.window, state_, False,
                                        None, self, '',
                                        int(self._box_rect.x + \
                                        self._div_width * i + \
                                        self._div_width / 2 - size_[0] / 2),
                                        self._box_rect.y + \
                                        self._box_rect.height,
                                        self._layout)


        # Line
        cr.set_line_width(max(width / 8, 0.5))
        cr.set_source_rgb(0.4, 0.4, 0.4)
        cr.move_to(self._box_rect.x + 1, y)
        cr.line_to(self._box_rect.width + self._box_rect.x, y)
        cr.stroke()

        mx, my = self.get_pointer()

        # Arrows
        arrow_y = self._box_rect.y + self._box_rect.height / 2 - 5
        ## left arrow
        self.style.paint_arrow(self.window, self.state, gtk.SHADOW_IN,
                               None, self, '', gtk.ARROW_LEFT, True,
                               self._box_rect.x - 15,
                               arrow_y,
                               8, 10)

        ## right arrow
        self.style.paint_arrow(self.window, self.state, gtk.SHADOW_IN,
                               None, self, '', gtk.ARROW_RIGHT, True,
                               self._box_rect.x + self._box_rect.width + 9,
                               arrow_y,
                               8, 10)

        # Focus rect
        if self.get_property('has-focus'):
            self.style.paint_focus(self.window, self.state, None, self, '',
                                   1,
                                   1,
                                   self.width - 2,
                                   self.height -2)
        

    def do_key_press_event(self, event):
        if event.hardware_keycode == 102 and event.state == gtk.gdk.CONTROL_MASK:
            # Control+right - go to next month
            month = (self.value.month % 12) + 1
            year = self.value.year + (self.value.month) / 12
            self.select_month(month=month, year=year)
        elif event.hardware_keycode == 100 and event.state == gtk.gdk.CONTROL_MASK:
            # Control+left - go to prev month
            year = self.value.year - int(not self.value.month - 1)
            month = self.value.month - 1 + (self.value.year - year) * 12
            self.select_month(month=month, year=year)
        elif event.hardware_keycode in (102, 104):
            # right/down - scroll right
            self.scroll(gtk.gdk.SCROLL_RIGHT)
        elif event.hardware_keycode in (100, 98):
            # left/up - scroll left
            self.scroll(gtk.gdk.SCROLL_LEFT)
        elif event.hardware_keycode == 86:
            # "+" - zoom in
            self.display_days -= 2
        elif event.hardware_keycode == 82:
            # "-" - zoom out
            self.display_days += 2
        elif event.hardware_keycode == 97:
            # Home - go to Today
            self.value = datetime.date.today()
            self._value_changed()
        elif event.hardware_keycode == 99:
            # PageUp
            self.set_position(self.position - self.display_days)
            self.move(self.allocation.width / 2)
        elif event.hardware_keycode == 105:
            # PageDow 
            self.set_position(self.position + self.display_days)
            self.move(self.allocation.width / 2)
        self.queue_draw_area(0, 0, self.allocation.width, self.allocation.height)

    def do_button_release_event(self, event):
        mx, my = self.get_pointer()
        self.drag = False
        if event.button == 1:
            self._pressed = False
            # Stop the autoscroll trigger timer
            if self._timer:
                gobject.source_remove(self._timer)
                self._timer = None
            if mx > self._box_rect.x and \
              mx < self._box_rect.width + self._box_rect.x:
                if not self._dragged:
                    self.move(mx - self._div_width / 2)
                    gobject.timeout_add(self._scroll_delay, self._center_selection)
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
        mx, my = self.get_pointer()
        # Stop the autoscroll trigger timer
        if self._timer:
            gobject.source_remove(self._timer)
            self._timer = None
        if event.button == 1:
            if mx < self._box_rect.x:
                self.scroll(gtk.gdk.SCROLL_LEFT)
                # Start the autoscroll trigger timer
                self._timer = gobject.timeout_add(500, self.auto_scroll,
                                                  gtk.gdk.SCROLL_LEFT)
            elif mx > self._box_rect.width + self._box_rect.x:
                self.scroll(gtk.gdk.SCROLL_RIGHT)
                # Start the autoscroll trigger timer
                self._timer = gobject.timeout_add(500, self.auto_scroll,
                                                  gtk.gdk.SCROLL_RIGHT)
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
                self.set_position((self.display_days / 2) + (pos_ - self._clicked_position), True)
            else:
                self._dragged = False
        else:
            # TODO Improve tooltip
            if mx < self._box_rect.x or \
              mx > self._box_rect.x + self._box_rect.width or \
              my > self._box_rect.y + self._box_rect.height:
                self.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.HAND2))
            elif my > self._box_rect.y - self._bullet_radius / 3 + (self._box_rect.height - self._bullet_radius) / 2 and \
              my < self._box_rect.y + self._bullet_radius / 3  + (self._box_rect.height / 2) + self._bullet_radius:
                if self._mindex != int((mx - self._box_rect.x) / self._div_width):
                    self._mindex = int((mx - self._box_rect.x) / self._div_width)
                    if self._mindex > -1 and self._mindex < self.DIVS[self._type] and self._bullets[self._mindex]:
                        gobject.timeout_add(100, self.set_tooltip, self._bullets[self._mindex].tooltip)
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
        self._box_rect.y = 8
        self._box_rect.width = allocation.width - self._box_rect.x * 2
        self._box_rect.height = allocation.height - 33
        # Set Bullet radius
        if self._div_width - self._div_width / 4 > self._box_rect.height / 2:
            self._bullet_radius = (self._box_rect.height / 2) / 2
        else:
            self._bullet_radius = (self._div_width - self._div_width / 4) / 2
        
        return False

    def _dist_dates(self, first=None):
        """ Calculate dates for visible positions """
        if not first:
            selected = self.value
            if self._type == self.WEEK and selected.weekday() != 0:
                selected -= datetime.timedelta(days=selected.weekday())
            if self._type == self.DAY:
                first = selected - datetime.timedelta(days=self.position)
            elif self._type == self.WEEK:
                first = selected - datetime.timedelta(days=self.position * 7)
            elif self._type == self.MONTH:
                month = (selected.month - self.position) % 12
                year = selected.year + (selected.month - self.position) // 12
                if not month:
                    month = 12
                    year -= 1
                first = selected.replace(month=month, year=year)
            elif self._type == self.YEAR:
                first = selected.replace(year=selected.year - self.position)
                
        if self._type == self.DAY:
            for i in range(self._display_days + 1):
                self._dates[i] = first + datetime.timedelta(days=i)
                self._bullets[i] = self._bullet_func(self._dates[i])
        elif self._type == self.WEEK:
            for i in range(self._display_days + 1):
                self._dates[i] = first + datetime.timedelta(days=i * 7)
                self._bullets[i] = self._bullet_func(self._dates[i])
        elif self._type == self.MONTH:
            for i in range(self._display_days + 1):
                month = (first.month + i) % 12
                year = first.year + (first.month + i) // 12
                if not month:
                    month = 12
                    year -= 1
                self._dates[i] = first.replace(day=1, month=month, year=year)
                self._bullets[i] = self._bullet_func(self._dates[i])
        elif self._type == self.YEAR:
            for i in range(self._display_days + 1):
                self._dates[i] = first.replace(day=1, month=1,
                                               year=first.year + i)
                self._bullets[i] = self._bullet_func(self._dates[i])


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
            self.set_position(self.position + 1, redraw)
            self.emit('scroll', direction)
        elif direction == gtk.gdk.SCROLL_RIGHT:
            self.set_position(self.position - 1, redraw)
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
        self._timer = gobject.timeout_add(self._scroll_delay,
                                          self.scroll,
                                          direction, redraw)
        return False

    def _center_selection(self):
        if self.position > (self._display_days - 1) / 2:
            self.set_position(self.position - 1, True)
        elif self.position < (self._display_days - 1) / 2:
            self.set_position(self.position + 1, True)
        return self.position != self._display_days / 2
            
    def move(self, pos, update=True, redraw=True):
        position_old = self.position
        self.position = round((pos - self._box_rect.x) / self._div_width)
        x = self.position * self._div_width + self._box_rect.x
        if pos > x + self._div_width / 2:
            self.position += 1
            x += self._div_width
        self.queue_draw_area(0, 0,
                             self.allocation.width, self.allocation.height)
        if self.debug :
            if not self._dragged:
                print "Timeline.position: ", self.position

        if update:
            # Update self.value
            if self.position < 0 or self.position > self._display_days - 1:
                return
            self.value = self._dates[self.position]
            self._dist_dates()
            self._value_changed()
        return position_old, self.position

    def set_position(self, pos, redraw=True):
        self.position = round(pos)
        x = pos * self._div_width + self._box_rect.x
        self.move(x, False, redraw)
        self._dist_dates()
        return self.position

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
        elif days > 61:
            days = 61
        if days == days_old:
            return
        self._display_days = days
        self._dist_dates()
        # Set timeline subdivisions size
        self.on_size_allocate(self, self.allocation)
        self._center_selection()
        self.queue_draw_area(0, 0, self.allocation.width,
                                 self.allocation.height)
    display_days = property(get_display_days, set_display_days)

    def get_type(self):
        """ Return timeline type
            (Timeline.DAY, Timeline.WEEK, Timeline.MONTH or Timeline.YEAR)
        """
        return self._type

    def set_type(self, type):
        self._type = type
        self._display_days = self.DIVS[self._type]
        self._dist_dates()
        self.queue_draw_area(0, 0, self.allocation.width,
                             self.allocation.height)

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
        self._bullet_func = func

def bullet_cb(date):
    if debug:
        print date.day

    if date == datetime.date(2008, 9, 10):
        return Bullet(date, 50, False, 1, False, False, 'Tooltip')
    elif date == datetime.date(2008, 9, 20):
        return Bullet(date, 200, False, -1, True, True, 'Another tooltip')
    elif date == datetime.date(2008, 9, 29):
        return Bullet(date, 200, False, 1, True, False, 'Yep. This is a tooltip')
    elif date == datetime.date(2008, 10, 2):
        return Bullet(date, 20, True, 0, False, False, 'What? Ah, tooltip...')
    elif  date == datetime.date(2008, 10, 19):
        return Bullet(date, 700, False, 0, True, False, 'Do you really want more tooltip?')

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

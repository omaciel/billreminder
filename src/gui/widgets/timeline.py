#!/usr/bin/env python
#-*- coding:utf-8 -*-

import datetime
import locale
from math import pi, floor

import pygtk
pygtk.require("2.0")
import gtk
import gobject
import pango
import cairo

import graphics
from pytweener import Easing

class Event(graphics.Sprite):
    OVERDUE = int('001', 2)
    TO_BE_PAID = int('010', 2)
    PAID = int('100', 2)

    def __init__(self, date=None, radius=16, fill='#f00', stroke='#fff',
                 line_width=1, amountdue=0, payee='', estimated=False,
                 overthreshold=False, status=0, multi=0, tooltip='',
                 **kwargs):
        graphics.Sprite.__init__(self, **kwargs)

        if date:
            self.date = date
        else:
            self.date = datetime.date.today()

        self.radius = radius
        self.fill = fill
        self.stroke = stroke
        self.line_width = line_width

        self.amountdue = amountdue
        self.payee = payee
        self.estimated = estimated
        self.overthreshold = overthreshold
        self.status = status
        self.multi = multi
        self.tooltip = tooltip

        self.bullet_color = None

        self.rectangle = graphics.Rectangle(1, 1, 5,
                                           stroke='#fff',
                                           interactive=True)
        self.rectangle.connect("on-mouse-over", self.on_mouse_over)
        self.rectangle.connect("on-mouse-out", self.on_mouse_out)
        self.rectangle.connect("on-click", self.on_click)
        self.rectangle.mouse_cursor = gtk.gdk.ARROW
        self.rectangle.opacity = 0
        self.add_child(self.rectangle)

        self.payee_label = graphics.Label(self.payee, color='#fff')
        self.payee_label.x = 14
        self.add_child(self.payee_label)

        self.amount_label = graphics.Label(self.float_to_currency(
                                               self.amountdue),
                                           color='#fff')
        self.amount_label.x = 4
        self.amount_label.y = 14
        self.add_child(self.amount_label)

        self.connect("on-render", self.on_render)

    def on_mouse_over(self, sprite):
        self.parent.set_tooltip_text(self.tooltip)
        self.emit('on-mouse-over')

    def on_mouse_out(self, sprite):
        self.parent.set_tooltip_text(None)
        self.emit('on-mouse-out')

    def on_click(self, event, sprite):
        self.emit('on-click', event)

    def move_to_default_position(self):
        x, y = self.parent.get_date_coords(self.date)
        self.x = x + 4
        self.y = y + self.parent._middle - 7

    def on_render(self, sprite):
        #TODO make colors configurable
        if self.status == self.TO_BE_PAID:
            self.fill = '#008000'
        elif self.status == self.OVERDUE:
            self.fill = '#ff0000'
        elif self.status == self.PAID:
            self.fill =  '#b3b3b3'

        self.move_to_default_position()

        if self.multi:
            self.graphics.rectangle(2.5, 2.5, self.parent.item_width - 5,
                                    int(self.parent._font_height * 1.8) + 2,
                                    corner_radius=7)
            self.graphics.fill_stroke(self.fill, '#fff', self.line_width)

        self.graphics.rectangle(0.5, 0.5, self.parent.item_width - 6,
                                int(self.parent._font_height * 1.8),
                                corner_radius=5)
        self.graphics.fill_stroke(self.fill, '#fff', self.line_width)
        self.graphics.circle(7.5, 7.5, 3)
        self.graphics.fill_stroke((self.bullet_color if self.bullet_color else
                                   self.parent.style.text[self.parent.state]),
                                   self.parent.style.base[self.parent.state],
                                   self.line_width)

        self.rectangle.width = self.parent.item_width - 1
        self.rectangle.height = int(self.parent._font_height * 1.8) + 5

        if self.parent.item_width >= 52:
            self.style = gtk.Style()
            size = self.style.font_desc.get_size() / pango.SCALE
            family = self.style.font_desc.get_family()
            fontstyle = self.style.font_desc.get_style()
            weight = self.style.font_desc.get_weight()

            self.payee_label.font_desc.set_size((size - 1) * pango.SCALE)
            self.payee_label.font_desc.set_family(family)
            self.payee_label.font_desc.set_style(fontstyle)
            self.payee_label.font_desc.set_weight(weight)
            self.payee_label.max_width = self.parent.item_width - 22
            self.payee_label.text = self.payee

            self.amount_label.font_desc.set_size((size - 2) * pango.SCALE)
            self.amount_label.font_desc.set_family(family)
            self.amount_label.font_desc.set_style(fontstyle)
            self.amount_label.font_desc.set_weight(weight)
            self.amount_label.y = self.parent._font_height * 0.9
            self.amount_label.max_width = self.parent.item_width - 12
            self.amount_label.text = self.float_to_currency(self.amountdue)
        else:
            if self.multi and self.parent.item_width >= 25:
                self.amount_label.text = '%d' % self.multi
            else:
                self.amount_label.text = ''
            self.payee_label.text = ''

    @staticmethod
    def float_to_currency(number):
        format_ = "%%.%df" % locale.localeconv()['int_frac_digits']
        return locale.format(format_, number)


class TimelineBox(graphics.Scene):
    __gsignals__ = {
        'value-changed': (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE,
                          (gobject.TYPE_PYOBJECT,)),
        'event-added': (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE,
                        (gobject.TYPE_PYOBJECT,)),
        'cleared': (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE,
                    (gobject.TYPE_BOOLEAN,))
    }

    ZOOM_IN = 1
    ZOOM_OUT = -1

    DEBUG = False

    def __init__(self, start_date=None, count=7, callback=None):
        graphics.Scene.__init__(self, scale=False, keep_aspect=False,
                                framerate=60)

        if start_date:
            self._start_date = start_date
        else:
            self._start_date = datetime.date.today() - datetime.timedelta(3)

        self._event_function = callback

        self.value = self.start_date

        self.item_width = self.default_item_width = 62

        self.width = 400
        self.height = 50
        self.set_size_request(self.width, self.height)

        self.count = count

        self._stop = False
        self._scrolling = False
        self._pressed = False
        self._middle = 0

        self._scroll_awaiting = 0
        self._font_height = 17

        self._layout = self.create_pango_layout('')
        self._2_times_pi = 2 * pi

        # Sprite used as reference to draw and animete date boxes
        if self.DEBUG:
            self.reference = graphics.Circle(10, 10, '#0ff', x=0, y=10)
        else:
            self.reference = graphics.Circle(0, 0, '#fff', x=0, y=0)
        self.add_child(self.reference)

        # Define the scroll speed
        self._scroll_duration_factor = 300.0
        self._scroll_duration = self.item_width / self._scroll_duration_factor

        self.set_property('can-focus', True)

        self.connect('size-allocate', self._on_size_allocate)
        self.connect('on-enter-frame', self._on_enter_frame)
        # Prevent infinite auto scroll
        self.connect('focus-out-event', lambda *args: self.stop_auto_scroll())

        self.refresh()

    def clear(self):
        graphics.Scene.clear(self)
        self.emit('cleared', True)

    def refresh(self):
        if self._event_function:
            self.clear()

            total = self.count + 2
            for i in range(-1, total):
                date = self.start_date + datetime.timedelta(i)
                event = self._event_function(date, 0, True)
                if event:
                    self.add_event(event)
        else:
            self.move_all_sprites_to_default_position()

        self.redraw()

    def get_start_date(self):
        return self._start_date
    def set_start_date(self, date):
        self._start_date = date
        self.value_changed()
    start_date = property(get_start_date, set_start_date)

    def get_end_date(self):
        return self.start_date + datetime.timedelta((self.width /
                                                     self.item_width) - 1)
    def set_end_date(self, date):
        raise TypeError("property 'end_date' is not writable")
    end_date = property(get_end_date, set_end_date)

    def value_changed(self):
        self.value = self.start_date
        if (self._stop or self._scroll_awaiting == 1 or
            self._scroll_awaiting % 3 == 0):
            self.emit('value-changed', self.value)

        if self._event_function:
            event = self._event_function(self.start_date - datetime.timedelta(1), 0)
            if event:
                self.add_event(event)

            event = self._event_function(self.end_date + datetime.timedelta(1), 0)
            if event:
                self.add_event(event)

        #self.move_all_sprites_to_default_position()

    def scroll_left(self, sprite=None, auto=False, duration=None, days=1,
                    easing=Easing.Linear.ease_out):
        if not sprite:
            sprite = self.reference

        if not duration:
            duration = self._scroll_duration

        self._scrolling = True
        self._scroll_awaiting = days
        self.reference.old_x = self.reference.x

        def _scroll_left_next(sprite=None):
            if self.reference.x <= self.item_width:
                self.reference.x = 0
                self.reference.old_x = self.reference.x
                self.start_date -= datetime.timedelta(1)
                self._scroll_next(sprite, gtk.gdk.SCROLL_LEFT)

        def _scroll_left_stopped(sprite=None):
            self.start_date -= datetime.timedelta(1)
            self._scroll_stopped(sprite)

        self.animate(
            sprite, x=self.item_width,
            easing=easing,
            on_complete=_scroll_left_next if auto else _scroll_left_stopped,
            on_update=self._scroll_all_sprites,
            duration=duration
        )

    def scroll_right(self, sprite=None, auto=False, duration=None, days=1,
                     easing=Easing.Linear.ease_out):
        if not sprite:
            sprite = self.reference

        if not duration:
            duration = self._scroll_duration

        self._scrolling = True
        self._scroll_awaiting = days
        self.reference.old_x = self.reference.x

        def _scroll_right_next(sprite=None):
            if self.reference.x >= self.item_width * (-1):
                self.reference.x = 0
                self.reference.old_x = self.reference.x
                self.start_date += datetime.timedelta(1)
            self._scroll_next(sprite, gtk.gdk.SCROLL_RIGHT)

        def _scroll_right_stopped(sprite=None):
            self.start_date += datetime.timedelta(1)
            self._scroll_stopped(sprite)

        self.animate(sprite, x=self.item_width * (-1), easing=easing,
                     on_complete=(_scroll_right_next if auto else
                                  _scroll_right_stopped),
                     on_update=self._scroll_all_sprites, duration=duration)

    def _scroll_next(self, sprite=None, direction=None):
        if self._stop:
            self._scroll_stopped()
            return

        easing = Easing.Linear.ease_out
        duration = self._scroll_duration * 0.4

        if self._scroll_awaiting > 1:
            self._scroll_awaiting -= 1
            if self._scroll_awaiting > 2:
                duration = self._scroll_duration * 0.4
            self.stop_auto_scroll()

        if direction is gtk.gdk.SCROLL_LEFT:
            self.scroll_left(sprite, True, duration, self._scroll_awaiting,
                             easing)
        elif direction is gtk.gdk.SCROLL_RIGHT:
            self.scroll_right(sprite, True, duration, self._scroll_awaiting,
                              easing)

    def _scroll_stopped(self, sprite=None):
        self._stop = False
        self._scrolling = False
        self.reference.x = 0
        self.move_all_sprites_to_default_position()

    def _scroll_all_sprites(self, sprite=None):
        diff = self.reference.x - self.reference.old_x
        for s in self.sprites:
            if s is not self.reference:
                s.x += diff
        self.reference.old_x = self.reference.x

    def move_all_sprites_to_default_position(self):
        for s in self.sprites:
            if s is not self.reference:
                s.move_to_default_position()
                s.emit('on-render')

    def stop_auto_scroll(self):
        if self._scroll_awaiting <= 1 and self._scrolling:
            self._stop = True

    def get_date_coords(self, date):
        pos = (date - self.start_date).days
        return [pos * self.item_width + self.reference.x, 0]

    def add_event(self, sprite):
        self.add_child(sprite)
        self.emit('event-added', sprite)

    def zoom(self, zoom):
        if zoom is self.ZOOM_OUT:
            self.count += 1
        elif zoom is self.ZOOM_IN:
            self.count -= 1

        old_item_width = self.item_width
        self.item_width = self.default_item_width = self.width / self.count
        self._scroll_duration = self.item_width / self._scroll_duration_factor

        self.move_all_sprites_to_default_position()

        self.redraw()

        if self.width / old_item_width != self.width / self.item_width:
            self.value_changed()

        return True

    def can_zoom_in(self):
        return self.width / self.count < 150 and self.count > 1

    def can_zoom_out(self):
        return self.width / self.count > 20

    def zoom_in(self):
        if self.can_zoom_in():
            return self.zoom(self.ZOOM_IN)
        else:
            return False

    def zoom_out(self):
        if self.can_zoom_out():
            return self.zoom(self.ZOOM_OUT)
        else:
            return False

    def do_key_release_event(self, event):
        self.stop_auto_scroll()

    def do_key_press_event(self, event):
        if self._scrolling:
            return

        # "+" - zoom in
        if (gtk.gdk.keyval_name(event.keyval) == 'plus' or
            gtk.gdk.keyval_name(event.keyval) == 'KP_Add'):
            self.zoom_in()

        # "-" - zoom out
        elif (gtk.gdk.keyval_name(event.keyval) == 'minus' or
              gtk.gdk.keyval_name(event.keyval) == 'KP_Subtract'):
            self.zoom_out()

        elif event.state & gtk.gdk.CONTROL_MASK:
            month = self.start_date.month
            year = self.start_date.year
            if gtk.gdk.keyval_name(event.keyval) == 'Left':
                month -= 1
                if month == 0:
                    month = 12
            if month == 2:
                if year % 4:
                    days = 28
                else:
                    days = 29
            elif (month <= 7 and month % 2) or (month >= 7 and not month % 2):
                days = 31
            else:
                days = 30

            if gtk.gdk.keyval_name(event.keyval) == 'Left':
                self.start_date -= datetime.timedelta(days - 1)
                self.refresh()
                self.scroll_left(None, False, self._scroll_duration * 0.6)

            elif gtk.gdk.keyval_name(event.keyval) == 'Right':
                self.start_date += datetime.timedelta(days - 1)
                self.refresh()
                self.scroll_right(None, False, self._scroll_duration * 0.6)

        elif gtk.gdk.keyval_name(event.keyval) == 'Left':
            self.scroll_left(auto=True)

        elif gtk.gdk.keyval_name(event.keyval) == 'Right':
            self.scroll_right(auto=True)

        elif gtk.gdk.keyval_name(event.keyval) == 'Page_Up':
            self.start_date -= datetime.timedelta(self.count - 1)
            self.refresh()
            self.scroll_left(None, False, self._scroll_duration * 0.6)

        elif gtk.gdk.keyval_name(event.keyval) == 'Page_Down':
            self.start_date += datetime.timedelta(self.count - 1)
            self.refresh()
            self.scroll_right(None, False, self._scroll_duration * 0.6)


    def do_button_release_event(self, event):
        self._pressed = False
        self.mouse_cursor = None
        if self.reference.x == 0:
            return

        self.reference.old_x = self.reference.x

        if self.reference.x < 0:
            new_x = self.item_width * (-1)
        elif self.reference.x > 0:
            new_x = self.item_width

        def _on_complete(sprite=None):
            sprite.x = 0
            if self.reference.old_x > 0:
                self.start_date -= datetime.timedelta(1)
            else:
                self.start_date += datetime.timedelta(1)
            self.value_changed()

        if self.item_width == abs(self.reference.x):
            _on_complete(self.reference)
        else:
            self.animate(self.reference, x=new_x,
                         easing=Easing.Linear.ease_out,
                         on_complete=_on_complete,
                         on_update=self._scroll_all_sprites,
                         duration=(self._scroll_duration *
                                   (self.item_width - abs(self.reference.x)) /
                                   self.item_width))

    def do_button_press_event(self, event):
        if event.button == 1: # Clicked with the mouse left buttom
            self._pressed = True
            self._clicked_position = self.get_pointer()
            self.mouse_cursor = gtk.gdk.Cursor(gtk.gdk.FLEUR)

    def do_motion_notify_event(self, event):
        if self._pressed:
            mx, my = self.get_pointer()

            if self.reference.x <= self.item_width * (-1):
                self._clicked_position = (mx, my)
                self.reference.x += self.item_width
                self.start_date += datetime.timedelta(1)
            elif  self.reference.x >= self.item_width:
                self._clicked_position = (mx, my)
                self.reference.x -= self.item_width
                self.start_date -= datetime.timedelta(1)

            self.reference.old_x = self.reference.x
            self.reference.x = mx - self._clicked_position[0]

            if self.sprites:
                self._scroll_all_sprites()
            else:
                self.redraw()

    def do_on_scroll(self, event):
        if self._scrolling or self._stop:
            return

        if event.state & gtk.gdk.CONTROL_MASK:
            # Zoom in-ou if ctrl key is pressed
            old_item_width = self.item_width

            if ((event.direction is gtk.gdk.SCROLL_LEFT or
                 event.direction is gtk.gdk.SCROLL_UP) and
                self.item_width < 150 and self.count > 1):
                self.zoom_in()
            elif ((event.direction is gtk.gdk.SCROLL_RIGHT or
                   event.direction is gtk.gdk.SCROLL_DOWN) and
                  self.item_width > 20):
                self.zoom_out()
        else:
            # Scroll if ctrl key is not pressed
            if (event.direction is gtk.gdk.SCROLL_LEFT or
                event.direction is gtk.gdk.SCROLL_UP):
                self.scroll_left(duration=self._scroll_duration * 0.4)
            elif (event.direction is gtk.gdk.SCROLL_RIGHT or
                  event.direction is gtk.gdk.SCROLL_DOWN):
                self.scroll_right(duration=self._scroll_duration * 0.4)

    def _on_size_allocate(self, widget, allocation):
        self.width = allocation.width
        self.height = allocation.height

        self._middle = int(self.height / 2) + .5

        try:
            if self.width != self.old_width:
                self.count = int(self.width / self.default_item_width)
        except AttributeError:
            self.default_item_width = self.width / self.count

        self.item_width = self.width / self.count
        self.move_all_sprites_to_default_position()

        self.old_width = self.width

    def _on_enter_frame(self, scene, context):
        # Define the widget background using the system color
        if self.background_color != self.style.base[self.state]:
            self.background_color = self.style.base[self.state]
            self.redraw() # Fix the background color when theme is changed
            self.move_all_sprites_to_default_position() # Fix all sprites

            # Get the system foreground and background colors to use on some elements
            self._fg_color = self.colors.parse(self.style.text[self.state])
            self._bg_color = self.colors.parse(self.style.bg[self.state])
            self._bs_color = self.colors.parse(self.style.base[self.state])
            self._fg_color_selected = self.colors.parse(self.style.text[gtk.STATE_SELECTED])
            self._bg_color_selected = self.colors.parse(self.style.bg[gtk.STATE_SELECTED])

            self._layout = self.create_pango_layout('')

        self._layout.set_markup('AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqWwXxYyZz')
        size_ = self._layout.get_pixel_size()
        self._font_height = size_[1]

        self.set_size_request(400, self._font_height * 4)

        # Draw main line
        context.set_line_width(1)
        context.set_source_rgb(*self._fg_color)
        context.move_to(0, self._middle)
        context.line_to(self.width, self._middle)
        context.stroke()

        # Draw year label
        if self.end_date.year != self.start_date.year:
            self._layout.set_markup('<small>%s</small>' %
                                    self.start_date.strftime('%Y'))

            self.style.paint_layout(self.window, self.state, False, None,
                                    self, '', 1, 2, self._layout)

        self._layout.set_markup('<small>%s</small>' %
                                self.end_date.strftime('%Y'))

        size_ = self._layout.get_pixel_size()
        year_label_width = size_[0]
        self.style.paint_layout(self.window, self.state, False, None,
                                self, '', int(self.width -
                                              year_label_width - 2),
                                2, self._layout)

        # Draw date boxes
        today = datetime.date.today()
        total = int(self.width / self.item_width) + 2
        for i in range(-1, total):
            date = self.start_date + datetime.timedelta(i)

            context.move_to(self.reference.x + self.item_width * i + 15.5,
                            self._middle)
            context.arc(self.reference.x + self.item_width * i + 11.5,
                        self._middle, 3, 0, self._2_times_pi)

            context.set_line_width(1.5)

            if date != today:
                context.set_source_rgb(*self._fg_color)
                context.fill_preserve()
                context.set_source_rgb(*self._bs_color)
                context.stroke()
            else:
                context.set_source_rgb(*self._bs_color)
                context.fill_preserve()
                context.set_source_rgb(*self._fg_color)
                context.stroke()

            # Draw date label
            self._layout.set_markup('<small>%s</small>' %
                                    date.strftime('%b %d'))
            size_ = self._layout.get_pixel_size()

            if size_[0] > self.item_width - 4 or self.item_width < 45:
                if (date.day == 1 or
                    (i == 0 and self.end_date.year == self.start_date.year and
                     not (date + datetime.timedelta(1)).day == 1)):
                    x_ = int(self.reference.x + self.item_width * i + 4)
                    self._layout.set_markup('<small>%s</small>' %
                                            date.strftime('%b'))
                    size_ = self._layout.get_pixel_size()
                    if x_ < self.width - year_label_width - size_[0] - 2:
                        self.style.paint_layout(self.window, self.state,
                                                False, None, self, '',
                                                x_ if (x_ >= 4 and
                                                      (i > 0 or
                                                       (i == 0 and
                                                        date.day == 1))
                                                      ) else 4,
                                                1, self._layout)

                self._layout.set_markup('<small>%s</small>' %
                                        date.strftime('%d'))

                size_ = self._layout.get_pixel_size()

            self.style.paint_layout(self.window, self.state, False, None,
                                    self, '', int(self.reference.x +
                                                  self.item_width * i + 4),
                                    int(self._middle - size_[1] - 6),
                                    self._layout)

            if self.DEBUG:
                # Draw box position number on debug mode
                context.set_source_rgb(*self._fg_color)
                context.move_to(self.reference.x + self.item_width * i + 6.5,
                                12)
                context.show_text('pos: %d/%d' % (i, total))

                # Draw the reference sprite on debug mode
                self.reference.width = 5
                self.reference.height = 5

        # Draw timeline box shadow
        self.style.paint_shadow(self.window, self.state, gtk.SHADOW_IN,
                                None, self, '', 0, 0, self.width, self.height)

        # Draw focus rect
        if self.get_property('has-focus'):
            self.style.paint_focus(self.window, self.state, None, self, '',
                                   2, 2, self.width - 4, self.height - 4)

        context.rectangle(1, 1, self.width - 2, self.height - 2)
        context.clip()

class Timeline(gtk.HBox):
    __gsignals__ = {
        'value-changed': (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE,
                          (gobject.TYPE_PYOBJECT,)),
        'event-added': (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE,
                        (gobject.TYPE_PYOBJECT,)),
        'cleared': (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE,
                    (gobject.TYPE_BOOLEAN,))
    }

    def __init__(self, date=None, count=7, callback=None, debug=False):
        super(gtk.HBox, self).__init__()

        # Treat the parameter
        if date and not isinstance(date, datetime.date) and \
          isinstance(date, tuple) and len(date) == 3:
            date = datetime.date(date[0], date[1], date[2])
        else:
            date = datetime.date.today()

        self.set_border_width(3)

        self.connect('size-allocate', self._on_size_allocate)

        # Create Timeline box
        self.timeline_box = TimelineBox(count=count, callback=callback)
        self.timeline_box.connect('value-changed',
                                  lambda widget, *arg:
                                      self.emit('value-changed', *arg))
        self.timeline_box.connect('event-added',
                                  lambda widget, *arg:
                                      self.emit('event-added', *arg))
        self.timeline_box.connect('cleared',
                                  lambda widget, *arg:
                                      self.emit('cleared', *arg))

        self.refresh = self.timeline_box.refresh
        self.can_zoom_in = self.timeline_box.can_zoom_in
        self.can_zoom_out = self.timeline_box.can_zoom_out
        self.zoom_in = self.timeline_box.zoom_in
        self.zoom_out = self.timeline_box.zoom_out
        self.add_event = self.timeline_box.add_event

        # Create scroll buttons
        left_arrow = gtk.Arrow(gtk.ARROW_LEFT, gtk.SHADOW_IN)
        self.left_bttn = gtk.Button();
        self.left_bttn.add(left_arrow)
        self.left_bttn.set_relief(gtk.RELIEF_NONE)
        self.left_bttn.set_property('can-focus', False)
        self.left_bttn.connect('released', self._on_left_bttn_released)
        self.left_bttn.connect('pressed', self._on_left_bttn_pressed)

        right_arrow = gtk.Arrow(gtk.ARROW_RIGHT, gtk.SHADOW_IN)
        self.right_bttn = gtk.Button();
        self.right_bttn.add(right_arrow)
        self.right_bttn.set_relief(gtk.RELIEF_NONE)
        self.right_bttn.set_property('can-focus', False)
        self.right_bttn.connect('released', self._on_right_bttn_released)
        self.right_bttn.connect('pressed', self._on_right_bttn_pressed)

        self.add(self.left_bttn)
        self.add(self.timeline_box)
        self.add(self.right_bttn)

        self.set_child_packing(self.left_bttn, False, False, 0, gtk.PACK_START)
        self.set_child_packing(self.timeline_box, True, True, 0, gtk.PACK_START)
        self.set_child_packing(self.right_bttn, False, False, 0, gtk.PACK_START)

    def get_start_date(self):
        return self.timeline_box.start_date
    def set_start_date(self, date):
        self.timeline_box.start_date = date
    start_date = property(get_start_date, set_start_date)

    def get_end_date(self):
        return self.timeline_box.end_date
    def set_end_date(self, date):
        self.timeline_box.end_date = date
    end_date = property(get_end_date, set_end_date)

    def get_value(self):
        return self.timeline_box.value
    def set_value(self, date):
        self.timeline_box.value = date
    value = property(get_value, set_value)

    def get_count(self):
        return self.timeline_box.count
    def set_count(self, count):
        self.timeline_box.count = count
    count = property(get_count, set_count)

    def _on_size_allocate(self, widget, allocation):
        self.width = allocation.width
        self.height = allocation.height
        self.timeline_box.reference.x = 0

    def _on_left_bttn_released(self, widget):
        self.timeline_box.stop_auto_scroll()

    def _on_right_bttn_released(self, widget):
        self.timeline_box.stop_auto_scroll()

    def _on_left_bttn_pressed(self, widget):
        self.timeline_box.scroll_left(auto=True)

    def _on_right_bttn_pressed(self, widget):
        self.timeline_box.scroll_right(auto=True)


if __name__ == '__main__':
    window = gtk.Window()
    window.set_title('Timeline')
    window.set_default_size(500, 70)

    timeline = Timeline(debug=True)

    b1 = Event(datetime.date.today(), fill='#bbb')
    b1.payee = 'Payee 1'
    timeline.add_event(b1)

    b2 = Event(datetime.date.today() + datetime.timedelta(3), fill='#f22')
    b2.payee = 'Payee 2'
    timeline.add_event(b2)

    window.add(timeline)
    window.connect('delete-event', gtk.main_quit)

    window.show_all()
    gtk.main()

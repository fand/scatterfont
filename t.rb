#!/usr/bin/env ruby

require 'rexml/document'
require 'rexml/xpath'
require 'awesome_print'

d = REXML::Document.new(open(ARGV[0]))

REXML::XPath.match(d, "//glyph").each do |g|
  # g.add_attribute('yo', 123)
  d.delete_element '//glyph'
end

units = REXML::XPath.first(d, '//font-face').attribute('units-per-em').value.to_i


p units / 10


p d.to_s


d.write(open(ARGV[1], "w"))

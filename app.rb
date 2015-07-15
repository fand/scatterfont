#!/usr/bin/env ruby

require 'sinatra'
require_relative 'scatter'

configure do
  mime_type :svg, 'image/svg+xml'
  set :css_dir, File.dirname(__FILE__) + '/static'
  set :public_folder, File.dirname(__FILE__) + '/static'
end

get '/' do
  File.read 'static/index.html'
end

get "/favicon.ico" do
  File.read('./static/favicon.ico')
end

get '/:fontname.?:svg?' do
  content_type :svg
  scatterFont params['fontname']
end

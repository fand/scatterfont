#!/usr/bin/env ruby

require 'sinatra'
require_relative 'scatter'

set :public_folder, File.dirname(__FILE__) + '/static'

configure do
  mime_type :svg, 'image/svg+xml'
end

get '/' do
  File.read 'templates/index.html'
end

get '/:fontname' do
  content_type :svg
  scatterFont params['fontname']
end

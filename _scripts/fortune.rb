#!/usr/bin/env ruby

require "cgi"

COMMIT = "<a href=\"https://github.com/alip/alip.github.com/commit/#{ENV['GIT_HEAD'].strip}\">#{ENV['GIT_HEAD_SHORT'].strip}</a>"
def fortune
  `#{ENV['FORTUNE']} #{ENV['FORTUNE_FLAGS']} #{ENV['FORTUNE_LIST']}`.strip
end

def cookie
  CGI.escapeHTML fortune
end

File.open(ENV['FORTUNE_FILE'], 'w') do |f|
  f.puts <<EOF
<p class="git">Quoting git after #{COMMIT} on #{Time.now.strftime('%Y-%m-%dT%H:%M:%S%z')}:</p>
<blockquote class="git"><pre class="git">#{cookie}</pre></blockquote>
EOF
  $stderr.puts fortune
end

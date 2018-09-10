#!/home/vagrant/.rbenv/shims/ruby
require "find"

dir = "./html"

print "Content-type: text/html\n\n"
print <<END
    <html>
    <head>
    <title>ディレクトリ内ファイル一覧</title>
    </head>
    <body>
    <h1>Choropleth Maps</h1>
END

Find.find(dir) do |file|
    if file =~ /\.s?html$/ and FileTest::size?(file) > 100
        filename = file.sub(/^#{dir}\//, "")
        print "<a href=\"#{file}\">#{filename}</a><br>\n"
    end
end

print <<END
    </body>
    </html>
END

exit
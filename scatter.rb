require 'rexml/document'
require 'rexml/xpath'

def scatterFont(fontname='droidsans')

    # open src file
    filepath = "svg/" + fontname + ".svg"
    d = REXML::Document.new(open(filepath))

    units = REXML::XPath.first(d, '//font-face').attribute('units-per-em').value.to_i
    units_10 = units / 10

    k_list = []
    k_tmp = []

    REXML::XPath.match(d, "//glyph").each do |g|

        if g.has_attribute 'd'
            path = g.attribute 'd'

            # glitch vertex
            vs = path.split 'v'
            vs = vs..map_with_index do |v, i|
                next if i == 0
                if rand < 0.3
                    v = "v" + v
                else
                    v = "h" + v
                end
            end
            path = vs.to_a.join

            # glitch curves
            cs = path.split 'q'
            cs = cs.map_with_index do |c, i|
                next if i == 0
                if rand < 0.3
                    c = (
                        "q" +
                        rand(-units_10..units_10).to_s + " " +
                        rand(-units_10..units_10).to_s + " " +
                        rand(-units_10..units_10).to_s + " " +
                        rand(-units_10..units_10).to_s + " " +
                        "q" + c)
                else
                    c = "q" + c
                end
            end
            path = cs.to_a.join

            # add noises
            r = rand(0..100)
            if r % 3 != 0
                (r % 11).times do

                    if r < 50
                        path += ("v " + rand(-units..units).to_s +
                                 "h " + rand(-units..units).to_s)
                    else
                        path = ("v " +  rand(-units..units).to_s +
                                "h " +  rand(-units..units).to_s +
                                path)
                    end

                end
            end

            g.set_attribute('d', path)

        end

    end

    # output
    s = d.to_s

    # with codecs.open("./scattered.svg", "wb") as f:
    #     f.write(s)

    return s
end

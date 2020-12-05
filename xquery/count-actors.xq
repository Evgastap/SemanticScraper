let $input := doc("/Users/evgastap/Documents/Code Projects/SemanticScraper/export.xml")
(:let $input := doc("path-to-file"):)

for $actor in distinct-values($input//actor/@id)
let $name := distinct-values($input//actor[@id eq $actor]/name)
let $count := count($input//movie/actor[@id eq $actor])
order by $count descending

return concat($name, ": ", $count)
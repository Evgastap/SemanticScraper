let $input := doc("/Users/evgastap/Documents/Code Projects/SemanticScraper/export.xml")
(:let $input := doc("path-to-file"):)

for $genre in distinct-values($input//genre)
let $count := count($input//genre[text() eq $genre])
order by $count descending
return concat($genre, " ", $count)
let $input := doc("/Users/evgastap/Documents/Code Projects/SemanticScraper/export.xml")

for $actor in $input//actor
if(format-integer(substring($actor/dob)) < 1980) then
return $actor/dob
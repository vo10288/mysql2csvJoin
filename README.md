# mysql2csvJoin

select mov_dett.*, articoli.* FROM mov_dett LEFT JOIN articoli ON mov_dett.idarticolo = articoli.idarticolo INTO OUTFILE '/Users/CFDA_BOLOGNA/Desktop/falcopsExport/falcopos.csv' FIELDS TERMINATED BY ';' LINES TERMINATED BY '\n';




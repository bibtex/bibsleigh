#!/bin/sh

echo "WARNING: This takes over an hour!"
echo "Fixing umlauts..."
sed -i "" "s/&auml;/ä/g" $1
sed -i "" "s/&euml;/ë/g" $1
sed -i "" "s/&iuml;/ï/g" $1
sed -i "" "s/&ouml;/ö/g" $1
sed -i "" "s/&uuml;/ü/g" $1
sed -i "" "s/&yuml;/ÿ/g" $1
echo "Fixing umlauts on capitals..."
sed -i "" "s/&Auml;/Ä/g" $1
sed -i "" "s/&Euml;/Ë/g" $1
sed -i "" "s/&Iuml;/Ï/g" $1
sed -i "" "s/&Ouml;/Ö/g" $1
sed -i "" "s/&Uuml;/Ü/g" $1
sed -i "" "s/&Yuml;/Ÿ/g" $1
echo "Fixing acutes..."
sed -i "" "s/&aacute;/á/g" $1
sed -i "" "s/&eacute;/é/g" $1
sed -i "" "s/&iacute;/í/g" $1
sed -i "" "s/&oacute;/ó/g" $1
sed -i "" "s/&uacute;/ú/g" $1
sed -i "" "s/&yacute;/ý/g" $1
echo "Fixing acutes on capitals..."
sed -i "" "s/&Aacute;/Á/g" $1
sed -i "" "s/&Eacute;/É/g" $1
sed -i "" "s/&Iacute;/Í/g" $1
sed -i "" "s/&Oacute;/Ó/g" $1
sed -i "" "s/&Uacute;/Ú/g" $1
sed -i "" "s/&Yacute;/Ý/g" $1
echo "Fixing graves..."
sed -i "" "s/&agrave;/à/g" $1
sed -i "" "s/&egrave;/è/g" $1
sed -i "" "s/&igrave;/ì/g" $1
sed -i "" "s/&ograve;/ò/g" $1
sed -i "" "s/&ugrave;/ù/g" $1
sed -i "" "s/&ygrave;/ỳ/g" $1
echo "Fixing graves on capitals..."
sed -i "" "s/&Agrave;/À/g" $1
sed -i "" "s/&Egrave;/È/g" $1
sed -i "" "s/&Igrave;/Ì/g" $1
sed -i "" "s/&Ograve;/Ò/g" $1
sed -i "" "s/&Ugrave;/Ù/g" $1
sed -i "" "s/&Ygrave;/Ỳ/g" $1
echo "Fixing tildes..."
sed -i "" "s/&atilde;/ã/g" $1
sed -i "" "s/&otilde;/õ/g" $1
sed -i "" "s/&ntilde;/ñ/g" $1
echo "Fixing tildes in capitals..."
sed -i "" "s/&Atilde;/Ã/g" $1
sed -i "" "s/&Otilde;/Õ/g" $1
sed -i "" "s/&Ntilde;/Ñ/g" $1
echo "Fixing rings and circumflexes..."
sed -i "" "s/&aring;/å/g" $1
sed -i "" "s/&acirc;/â/g" $1
sed -i "" "s/&ccirc;/ĉ/g" $1
sed -i "" "s/&ecirc;/ê/g" $1
sed -i "" "s/&icirc;/î/g" $1
sed -i "" "s/&ocirc;/ô/g" $1
sed -i "" "s/&ucirc;/û/g" $1
echo "Fixing rings and circumflexes in capitals..."
sed -i "" "s/&Aring;/Å/g" $1
sed -i "" "s/&Acirc;/Â/g" $1
sed -i "" "s/&Ccirc;/Ĉ/g" $1
sed -i "" "s/&Ecirc;/Ê/g" $1
sed -i "" "s/&Icirc;/Î/g" $1
sed -i "" "s/&Ocirc;/Ô/g" $1
sed -i "" "s/&Ucirc;/Û/g" $1
echo "Fixing other diacritics..."
sed -i "" "s/&ccedil;/ç/g" $1
sed -i "" "s/&Ccedil;/Ç/g" $1
sed -i "" "s/&oslash;/ø/g" $1
sed -i "" "s/&Oslash;/Ø/g" $1
echo "Fixing fancy letters..."
sed -i "" "s/&micro;/µ/g" $1
sed -i "" "s/&szlig;/ß/g" $1
sed -i "" "s/&aelig;/æ/g" $1
sed -i "" "s/&AElig;/Æ/g" $1
sed -i "" "s/&oelig;/œ/g" $1
sed -i "" "s/&OElig;/Œ/g" $1
sed -i "" "s/&eth;/ð/g" $1
sed -i "" "s/&ETH;/Ð/g" $1
sed -i "" "s/&thorn;/þ/g" $1
sed -i "" "s/&THORN;/Þ/g" $1
echo "Fixing miscellaneous signs..."
sed -i "" "s/&times;/×/g" $1
sed -i "" "s/&reg;/®/g" $1

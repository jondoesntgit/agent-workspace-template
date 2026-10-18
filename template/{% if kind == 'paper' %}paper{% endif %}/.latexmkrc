# Let LaTeX find the shared team style in standards/latex/.
# Build from this folder:  latexmk main.tex
ensure_path('TEXINPUTS', '../standards/latex//');
$pdf_mode = 1;

# Don't fail the build just because there are no citations yet (fresh documents).
$bibtex = 'internal team_bibtex %B';
sub team_bibtex {
    my $base = shift;
    my $ret = system('bibtex', $base);
    if ($ret != 0 && open(my $fh, '<', "$base.blg")) {
        local $/; my $log = <$fh>; close $fh;
        return 0 if $log =~ /I found no \\citation commands/;
    }
    return $ret;
}

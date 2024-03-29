\version "2.18.2"
\header {
	title = "my_drum_demo2"
	composer = "  "
	tagline = ##f
}

#(define harald '(
	(bassdrum        default   #f           -3)
	(snare           default   #f            1)
	(sidestick       cross     #f            1)
	(himidtom        default   #f            3)
	(lowtom          default   #f           -1)
	(hihat           cross     #f            5)
	(openhihat       cross     "open"        5)
	(pedalhihat      cross     #f           -5)
	(crashcymbal     cross     #f            6)
	(ridecymbal      cross     #f            4)
	(ridebell        diamond   #f            4)))
	% The number is 'semitones away from the middle staff (0)'

drum = \drummode {
	\set DrumStaff.drumStyleTable = #(alist->hash-table harald)
	\stemUp
	\override Beam #'damping = #+inf.0 % set beams horizontal
	\set Score.proportionalNotationDuration  = #(ly:make-moment 1/32)
	% Change to numeric style
	\numericTimeSignature
	\time 4/4
	\tempo 4 = 70
	% Disable beamExceptions because they are definitely
	% defined for 4/4 time
	\set Timing.beamExceptions = #'()
	\set Timing.baseMoment = #(ly:make-moment 1/4)
	\set Timing.beatStructure = #'(1 1 1 1)
	r 8  <bd >8  <sn >8  <sn >8  <bd sn >8  <sn >8  <sn >8  <bd sn >8  | 
 <sn >8  <sn >8 <bd sn >8  <bd sn >8  <bd sn >8  <sn >8  <sn >8  <bd sn >8  | 
 <bd sn >8  <sn >8 <bd sn >8  <bd sn >8  <sn >8  <sn >8  <sn >8  <bd sn >8  | 
 <sn >8  <sn >8 <bd sn >16  <bd sn >16  <bd >8  <bd sn >8  <bd sn >8  <sn >16  <sn >16  <sn >16  <bd sn >16  | 
 <bd sn >8  <bd sn >8 <sn >8  <sn >8  <sn >8  <sn >8  <sn >8  <bd sn >8  | 
 <sn >8  <sn >8 <sn >8  <bd sn >8  <sn >8  <sn >8  <sn >8  <sn >8  | 
 <sn >8  <sn >16  <sn >16 <bd sn >16  <bd sn >16  <bd sn >8 r8^"(four)"  <bd sn >8  | 
 <sn >8  <sn >8  <sn >8  <sn >8  | 
 <bd sn >16  <sn >16  <sn >8  <sn >16  <sn >16  <sn >8  <bd sn >16  <bd sn >16  <bd sn >16  <bd sn >16  <bd sn >16  <bd sn >16  <sn > 
}

lyric = \lyricmode {
	'n three 'n four 'n One 'n two 'n three 'n four 'n One 'n two 'n three 'n four 'n One 'n two 'n three e 'n four 'n One e 'n a two 'n three 'n four 'n One 'n two 'n three 'n four 'n One 'n two 'n a three e 'n 'n One 'n two 'n three e 'n four e 'n One e 'n a two e 'n 
}

\score {
<<
\new DrumStaff{
\new DrumVoice = "mydrums" { \drum }
}
\new Lyrics \lyricsto "mydrums" { \lyric }
>>
}


% bassdrum bd
% snare sn
% sidestick ss
% himidtom tommh
% lowtom toml
% closedhihat hhc
% openhihat hho
% pedalhihat hhp
% crashcymbal cymc
% ridecymbal cymr
% ridebell rb

% Harald Huyssen notation
% Crash: first ledger line above 
% Ride: above the top line
% Hihat: through the top staff
% Rack tom: top space
% Floor tom: second space from below

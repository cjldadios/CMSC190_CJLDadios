\version "2.18.2"
\header {
	title = "my_drum_demo"
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
	   <ss cymc >8  <sn rb >16  <bd sn tommh hhp >16 <bd ss rb hhp >8  <ss hh >8  <cymc hh >16  <bd ss toml >16  <bd sn >8  <sn tommh >8  <ss hh >8  | 
 <bd ss toml hhp >8  <bd tommh hh >16  <bd toml hh >16 <bd sn >8  <hh >8  <rb hh >16  <bd tommh >16  <bd tommh toml hhp >8  <sn tommh >8  <hh >8  | 
 <bd toml hh >8  <ss tommh >16  <tommh hh >16 <sn tommh >8  <hh >8  <rb hh >16  <bd toml hh >16  <sn tommh >8  <sn tommh >8  <ss hh >8  | 
 <ss tommh >8  <bd ss toml hhp >16  <bd tommh hh >16 <bd sn >8  <hho >8  <hho >16  <toml hho >16  <sn hho >8  <bd tommh toml hhp >16  <bd tommh toml hhp >16  <bd ss toml hhp >8  | 
 <bd ss rb hhp >8  <sn hh >16  <bd tommh hho >16 <bd ss cymr >8  <hh >8  <rb hh >16  <bd tommh rb hhp >16  <bd ss cymr hhp >8  <sn tommh >8  <hh >8  | 
 <bd ss toml hhp >8  <tommh cymr >16  <bd tommh toml hhp >16 <sn tommh >8  <cymc hh >8  <cymc hh >16  <toml hh >16  <bd toml cymr hhp >8  <bd ss rb >8  <cymc hh >8  | 
 <tommh toml >16  <toml hh >16  <sn toml >16  <tommh toml >16 <bd sn cymc >4  <hh >16  <tommh hh >16  <bd toml cymr hhp >8  <sn hh >8  <cymr hh >8  | 
 <tommh hho >8  <bd sn cymr hhp >16  <bd sn hho >16 <toml hho >8  <hho >16  <sn hh >16  <bd sn cymc >8  <tommh toml >16  <bd rb >16  <bd sn ss >16  <sn tommh >16  <toml hh >8  | 
 <bd sn hho >4 
}

lyric = \lyricmode {
	One 'n a two 'n three e 'n four 'n One 'n a two 'n three e 'n four 'n One 'n a two 'n three e 'n four 'n One 'n a two 'n three e 'n four e 'n One 'n a two 'n three e 'n four 'n One 'n a two 'n three e 'n four 'n One e 'n a two three e 'n four 'n One 'n a two 'n a three 'n a four e 'n One 
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

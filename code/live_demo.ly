\version "2.18.2"
\header {
	title = "live_demo"
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
	\tempo 4 = 89
	% Disable beamExceptions because they are definitely
	% defined for 4/4 time
	\set Timing.beamExceptions = #'()
	\set Timing.baseMoment = #(ly:make-moment 1/4)
	\set Timing.beatStructure = #'(1 1 1 1)
	   <bd sn toml hhp >4 <bd rb hh >16  <bd ss rb >8.  <ss tommh >8.  <bd tommh >16  | 
 <bd ss tommh >16  <bd toml hh >8.  <bd sn >8  <bd ss >8  <bd ss rb >8.  <bd ss rb >16  | 
 <bd ss rb hhp >16  <bd ss rb >8.  <bd toml cymr hhp >8.  <bd tommh >16  | 
 <bd ss >16  <bd toml >8.  <bd sn >8  <bd toml rb hhp >8  <bd ss cymr >8.  <bd sn tommh hhp >16  | 
 <bd ss rb hhp >16  <bd sn tommh >8.  <bd toml cymr hhp >8  <bd toml >16  <bd sn tommh >16  <bd tommh >16  <bd ss >8  <bd sn tommh >16  | 
 <bd sn >16  <tommh cymr >8  <bd ss cymr >16  <bd ss cymr hhp >16  <bd sn tommh hhp >8. r8.^"(one)"  <bd ss cymr >16  | 
 <bd sn >16  <bd sn rb hhp >8  <bd toml cymr hhp >16  <bd sn rb hhp >16  <toml cymr >8  <bd sn cymr >16  <bd tommh cymr hhp >16  <bd ss rb hhp >8  <bd toml cymr hhp >16  | 
 <sn tommh >16  <bd sn toml >16  <bd ss cymr >8  <sn tommh >4  <bd ss tommh hhp >8.  <bd sn >16  | 
 <bd sn ss >8  <bd ss >16  <bd ss rb >16r8.^"(one)"  <bd ss toml >16  <sn tommh >8.  <bd sn hh >16  | 
 <sn toml >8.  <bd sn hh >16  <bd sn ss >8.  <bd toml rb hhp >16  | 
 <bd ss cymr >4 <bd ss rb >8.  <bd ss toml >16  <sn toml >8.  <bd ss cymr >16  | 
 <bd sn >8.  <bd sn hh >16  <sn ss >8.  <bd toml rb hhp >16  | 
 <bd ss rb >8.  <bd sn >16 <bd sn hh >8.  <bd sn hh >16  <bd sn ss >8.  <bd sn toml >16  | 
 <bd toml rb hhp >8.  <bd ss toml >16  <sn toml >8.  <bd sn rb >16  | 
 <bd sn rb >8.  <bd toml rb >16  <bd sn >16  <bd sn hh >8  <bd sn >16  <bd ss tommh hhp >16  <toml rb >8.  | 
r16^"(two)"  <bd sn ss hhp > 
}

lyric = \lyricmode {
	One two e three a four e One 'n two a three e four a One e two 'n three a four e One 'n a two e a three e a four e a two e a three e a four e a One e 'n two three a four 'n a a two a three a four a One two a three a four a One a two a three a four a One a two a three a four e a One e e 
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

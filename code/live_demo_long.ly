\version "2.18.2"
\header {
	title = "live_demo_long"
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
	\tempo 4 = 67
	% Disable beamExceptions because they are definitely
	% defined for 4/4 time
	\set Timing.beamExceptions = #'()
	\set Timing.baseMoment = #(ly:make-moment 1/4)
	\set Timing.beatStructure = #'(1 1 1 1)
	   <bd hh >16  <bd hh >8. <bd toml >8.  <bd toml >16  <sn tommh >16  <bd ss >8  <bd hh >16  | 
 <bd toml >8  <bd toml cymr hhp >8 r8^"(one)"  <bd tommh >16  <bd toml >16  <bd hh >4  <bd toml >8.  <bd >16  | 
 <bd sn tommh >16  <bd tommh toml hhp >8  <bd toml >16  <bd tommh toml hhp >8  <bd tommh >16  <bd hh >16 r16^"(two)"  <bd toml >8  <bd sn >16  | 
 <bd rb hh >16  <bd toml cymr >8. r16^"(four)"  <bd ss toml >8.  | 
r16^"(one)"  <bd toml cymr hhp >16  <bd sn ss hhp >8  | 
r16^"(two)"  <bd toml cymr hhp >8  <bd tommh >16  <bd sn hh >8.  <bd toml >16  <bd hh >16  <bd toml cymr hhp >8  <bd ss rb hhp >16  | 
r8.^"(one)"  <bd sn toml >16 r16^"(two)"  r8  <bd toml cymr hhp >16  <bd sn toml >8.  <bd sn hh >16  | 
r16^"(four)"  <bd sn toml >8.  | 
r16^"(one)"  <bd >16  <bd sn >8  <bd toml cymr hhp >4  | 
 <bd sn tommh >4  <bd sn tommh >16  <bd sn >8  <bd sn toml >16  <bd sn ss >8.  <bd sn >16  | 
r8.^"(two)"  <bd toml >16  <bd toml cymr hhp >16  <bd toml cymr hhp >8. r16^"(four)"  <bd sn tommh >8.  | 
 r16  <bd sn tommh >16  <bd sn >8  | 
 <bd sn >4  <sn toml >8.  <bd sn tommh >16  | 
 <bd sn tommh >16  <bd rb hh >8  <bd toml cymr hhp >16 r8^"(one)"  <bd tommh >8 r16^"(two)"  <bd ss toml >16  <bd ss toml >8  <bd sn >16  <bd tommh >8  <bd tommh rb >16  | 
r16^"(four)"  <bd sn toml >8.  | 
 <bd toml cymr hhp >16  <bd sn >8  <bd sn >16  <bd rb hh >4  | 
 <bd ss >8.  <bd tommh >16  <bd hh >16  <bd sn tommh >8  <bd rb hh >16  <bd cymr hh >8  <bd ss hh >8  | 
r16^"(two)"  <bd tommh >16  <bd tommh >8  <bd sn toml >16  <bd tommh rb >8. r16^"(four)"  <bd tommh toml hhp >8.  | 
 <bd tommh >16  <bd hh >8.  | 
 <bd tommh toml >8.  <bd toml >16  <bd ss >16  <bd toml >8  r16  | 
 <bd toml >8  <bd sn ss >16  <bd rb hh >4 r16  <bd ss rb hhp >4  <bd sn >4  | 
r16^"(four)"  <bd sn hh >8  <bd sn tommh hhp >16  | 
 <bd sn rb hhp >16  <bd tommh rb >16  <bd ss rb hhp >8  <bd ss cymr >4  <bd ss rb hhp >16  <bd ss cymr >8.  | 
 <bd ss tommh >8  <bd ss toml >8 r16^"(one)"  <bd tommh >8  <bd toml >16  <bd ss cymr >4  | 
 <bd sn hh >4  <bd sn ss >16  <bd sn hh >8.  <bd toml cymr hhp >8  <bd sn tommh >8  | 
 <bd tommh toml >8.  <bd toml >16 <ss toml >8.  <bd rb hh >16  <bd sn >4  | 
 <bd ss rb >16  <bd tommh >8.  <bd toml cymr hhp >8.  <bd ss hh >16  | 
 <bd sn toml >8.  <bd toml >16 <bd toml rb hhp >4  <bd sn tommh hhp >4  <bd sn ss >16  <bd tommh >8.  | 
 <bd sn ss hhp >8.  <bd sn toml >16  <bd tommh cymr >8.  <bd tommh >16  | 
 <bd sn toml >4  <bd sn toml hhp >8.  <bd sn toml >16  <bd rb hh >16  <bd ss rb hhp >8.  | 
 <toml hh >8.  <bd sn toml >16  <bd ss hh >16  <bd toml >8.  | 
 <bd sn >8  <bd sn >8  <bd toml rb hhp >8.  <bd ss rb >16  <bd ss rb >16  <bd ss rb >8.  | 
 <bd toml cymr hhp >8.  <bd ss rb >16  <bd ss >16  <bd toml cymr hhp >8.  | 
 <bd sn toml >8  <bd toml cymr hhp >8  <bd ss cymr >8.  <tommh rb >16  <bd ss rb hhp >16  <bd toml rb >8.  | 
 <bd toml cymr hhp >16  <bd toml >8  <bd sn toml >16  <bd sn >16  <bd toml hh >8  <bd sn tommh >16  <bd sn >16  <sn rb >8  <bd tommh rb hhp >16  | 
r16^"(one)"  <bd sn hh >8. r8.^"(two)"  <bd ss cymr >16  | 
 <bd sn toml >16  <bd cymr hh >8  <bd toml cymr hhp >16 <bd toml cymr hhp >16  <toml cymr >8  <bd tommh cymr hhp >16  <sn tommh >16  <bd sn tommh hhp >8  <bd toml cymr hhp >16  <bd ss rb hhp >8.  <bd ss tommh hhp >16  | 
 <bd ss cymc hhp >4  <bd sn ss >8.  <bd sn hh >16  <bd ss cymr >8  <bd sn tommh >16  <bd ss rb >16  | 
r8.^"(two)"  <bd ss toml >16  <sn tommh >8.  <bd sn hh >16  | 
 <bd ss cymr >8.  <bd tommh toml hhp >16 <bd sn tommh hhp >8.  <bd sn hh >16  <bd ss cymr >8.  <bd ss rb >16  | 
 <bd tommh toml hhp >8.  <bd ss rb >16  <bd sn ss >8.  <bd ss tommh hhp >16  | 
 <bd sn ss >8.  <bd sn hh >16  <bd sn ss hhp >8.  <bd sn hh >16  | 
 <bd ss rb >8.  <bd ss rb >16  <bd ss tommh hhp >8.  <bd ss rb >16  <sn tommh >8.  <bd ss rb >16  | 
 <bd tommh toml hhp >8.  <bd sn hh >16  <sn tommh >8.  <bd sn rb >16  | 
 <bd toml rb hhp >8.  <bd sn hh >16  <bd sn >16  <sn tommh >8  <sn >16  <sn tommh >16  <bd ss cymr hhp >8.  | 
 <bd sn >16  <toml rb > 
}

lyric = \lyricmode {
	One e two a three e a four 'n 'n a two three a four e a One 'n a e a three e e e 'n e a three a four e a a a three a e e 'n two three four e a One a a three e e e 'n two three a four e a 'n e 'n three e a e One e a two three a four e a One 'n e 'n three e e One e two a three e four 'n a two three e a One e 'n two three e four 'n e a two three four e One 'n two a three a four One e two a three a four One two e three a four a One two a three e four a One e two 'n three a four e One a two e three 'n four a One e two e a three e a four e a e a three e a four e a One e a two a three four a One 'n a a three a four a One a two a three a four a One a two a three a four a One a two a three a four a One e a two e three e 
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

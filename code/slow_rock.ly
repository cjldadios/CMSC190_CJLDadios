\version "2.18.2"
\header {
	title = "slow_rock"
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
	\tempo 4 = 76
	% Disable beamExceptions because they are definitely
	% defined for 4/4 time
	\set Timing.beamExceptions = #'()
	\set Timing.baseMoment = #(ly:make-moment 1/4)
	\set Timing.beatStructure = #'(1 1 1 1)
	   <ss hh >4 <ss hh >4  r16  <bd >16  <bd >8  <bd >16  <bd >16  <bd >8  | 
 <bd rb >4 <bd hh >4  <bd cymr >8  <sn hh >8  <sn >8.  r16  | 
 <bd hh >8  <sn hh >8  <bd hh >4  <bd hh >8  <sn >8  <bd rb >8  <ss hh >16  r16  | 
 <bd hh >4  <bd rb >4  <bd rb >8  <ss hh >8  <sn >8.  r16  | 
 <bd rb >8  <ss hh >8  <bd >8.  <bd >16  | 
 r16  <bd cymc >8.  <bd hh >4  <bd hh >4  | 
 <bd >8  <sn hh >16  r16 <bd hh >4  <bd hh >8  <sn hh >8  <bd cymr >8  <sn hh >8  | 
 <bd cymc >8  <ss hh >16  r16 <bd >4  <bd >8  <sn hh >8  <bd cymr >8  <sn hh >8  | 
 <bd >8  <sn >16  <bd cymc >16 <bd hh >8  <ss hh >8  <bd >8  <ss hh >8  <sn >8  <ss hh >8  | 
 <bd cymc >4 <bd >16  <bd >8  r16  <bd >4  <bd cymc >4  | 
 <sn >4 <bd hh >8  <sn hh >8  <bd hh >8  <bd hh >16  <bd cymc >16  <bd hh >8  <sn hh >8  | 
 <bd hh >8  <sn hh >8 <bd hh >4  <bd hh >8.  <bd hh >16  <bd rb >4  | 
 <bd >4  <bd cymr >8  <ss hh >8  <bd >8.  r16  | 
 <bd rb >8  <sn >8  <bd >4  <bd >16  r16  <bd >16  <bd >16  <bd >8  <bd rb >8  | 
 <bd hh >4  <bd >8.  <bd hh >16  <bd rb >8  <ss hh >8  | 
 <bd rb >4  <bd cymr >8  <ss hh >8  <sn >8.  r16  | 
 <bd rb >8  <sn hh >8 <bd hh >8  <sn hh >16  <bd hh >16  <bd hh >4  <bd >8  <sn hh >8  | 
 <bd rb >8  <sn hh >8 <sn >8  <sn hh >16  <bd >16  <bd rb >8  <ss hh >8  <bd >16  r16  <bd >8  | 
 <bd >8  <bd >16  <bd >16 <bd rb >8  <sn >8  <bd cymr >4  <bd cymr >8  <ss hh >8  | 
 <bd hh >8  <ss hh >8 <bd >8  <ss hh >16  <bd >16  r8  <ss hh >8  <bd >8  <ss hh >16  <bd >16  | 
 r8  <ss hh >8 <bd >16  <bd >16  <toml cymr >16  <bd >16  <bd >8  <sn hh >8  <bd >8  <ss hh >16  <bd hh >16  | 
 r8  <bd hh >8 <bd >8  <ss hh >16  <bd >16  r8  <bd hh >8  <bd >8  <sn >16  <bd >16  | 
 r8  <bd hh >8 <bd >16  <bd hh >16  <toml cymr >16  <bd >16  <bd hh >8  <toml cymr >8  <bd >8  <ss hh >16  <tommh >16  | 
 <bd >8  <toml cymr >8 <bd >8  <ss hh >16  <bd >16  <bd hh >8  <ss hh >8  <bd >8  <ss hh >16  <bd hh >16  | 
 r8  <bd hh >8 <bd >16  <bd >16  <bd hh >16  <bd >16  <bd cymr >8  <ss hh >8  <bd >8  <ss hh >8  | 
 <bd hh >8  <ss hh >8 <bd >8  <ss hh >16  <bd hh >16  r8  <toml cymr >8  <bd >8  <bd hh >16  <tommh >16  | 
 <bd >8  <toml cymr >8 <bd >16  <sn >16  <sn >8  <bd hh >4  <bd hh >8.  r16  | 
 <bd hh >8  <ss hh >8  <bd >8  <sn hh >16  <bd >16  <bd >8  <toml cymr >8  <bd hh >8  <ss hh >16  <bd >16  | 
 r8  <ss hh >8  <bd >16  <bd cymr >8  <bd >16  <bd rb >4  r8  <ss hh >8  | 
 <bd hh >8  <sn >8  <bd >8  <ss hh >16  <bd >16  r8  <ss hh >8  <bd hh >8  <ss hh >16  <tommh >16  | 
 <bd rb >8  <sn >16  r16  <bd >16  <bd >16  <bd >8  <bd cymc >4  <bd rb >8  <ss hh >16  <bd >16  | 
 <bd hh >8  <ss hh >8  <bd >8  <sn >16  <tommh >16  <bd >8  <toml cymr >8  <bd >8  <ss hh >16  <bd hh >16  | 
 <bd hh >8  <toml cymr >8  <bd >16  <tommh >16  <bd rb >16  <bd >16  <sn >8  <ss hh >8  <bd >8  <toml cymr >16  <bd >16  | 
 <bd >8  <bd hh >8  <bd hh >8  <bd hh >16  <bd >16  r8  <ss hh >8  <bd >8  <ss hh >16  <bd >16  | 
 <bd >16  <bd >16  <tommh >8  <tommh >8  <bd >8  <bd cymc >4  <bd cymr >8.  <bd >16  | 
 <bd >8  <sn hh >8  <bd cymc >8.  <bd >16  | 
 <bd hh >8  <sn hh >8  <bd cymc >8.  r16  <bd rb >8  <sn hh >8  | 
 <bd >16  r16  <bd hh >16  <bd hh >16 r8  <sn hh >8  <bd cymc >8.  r16  <bd cymr >8  <ss hh >8  | 
 <bd hh >8  <toml cymr >16  <bd cymc >16  <bd rb >8  <sn hh >8  <bd hh >8  <sn hh >16  <bd >16  <bd rb >8  <ss hh >8  | 
 <bd cymc >16  <bd hh >16  <sn hh >16  <bd >16  <bd rb >4  <sn >8.  <bd cymc >16  | 
 <bd rb >4  <bd hh >8  <ss hh >16  <bd hh >16  <bd rb >8  <toml cymr >8  <bd >8  <toml cymr >16  <bd cymc >16  | 
 <bd cymr >16  <bd hh >16  <bd >8  <bd >16  <bd >16  r8  <bd rb >4  <bd rb >8.  <bd cymc >16  | 
 <bd cymr >8  <sn hh >8  <bd hh >8.  r16  | 
 <bd hh >8  <ss hh >8 <sn >8  <ss hh >16  r16  <bd >16  <bd >16  r8  <bd >8  <sn >8  | 
 <bd hh >4 <bd cymr >8.  <bd cymc >16  <bd hh >8  <toml cymr >8  <bd hh >8.  <bd hh >16  | 
 <bd rb >8  <sn hh >8  <sn >8  <ss hh >16  <bd hh >16  <sn >8  <ss hh >16  <bd >16  | 
 <bd >16  <bd >16  <bd >16  r16  <bd cymr >4  <bd hh >8  <toml cymr >16  <bd cymc >16  <bd hh >8  <sn hh >8  | 
 <bd cymc >8  <sn >16  <bd >16  <bd cymr >8  <ss hh >8  <bd rb >8  <sn >16  <bd >16  <bd >8  <bd rb >16  <bd hh >16  | 
 <bd cymr >8  <bd rb >8  <bd hh >8  <ss hh >8  <bd hh >8  <bd hh >16  <bd >16  r8  <ss hh >8  | 
 <bd >8  <bd hh >16  <bd >16  <bd >8  <ss hh >8  <bd >8  <ss hh >16  <bd >16  r8  <bd hh >8  | 
 <bd hh >16  <bd >16  <sn >16  <bd hh >16  <bd cymc >8  <toml cymr >8  <bd >8  <ss hh >16  <bd >16  <bd >8  <toml cymr >8  | 
 <bd hh >8  <ss hh >16  <bd >16  r8  <bd hh >8  <bd >8  <ss hh >16  <tommh >16  <bd hh >8  <ss hh >8  | 
 <bd cymc >16  <bd >16  <sn hh >16  r16  <bd >8  <bd hh >8  <bd >8  <ss hh >16  <bd >16  <tommh >8  <ss hh >8  | 
 <bd >8  <ss hh >16  <bd >16  <bd hh >8  <sn >8  <bd hh >8  <bd hh >16  <bd >16  <bd hh >8  <bd hh >8  | 
 <bd >16  <bd hh >16  <bd hh >16  <bd >16  r8  <bd hh >8  <bd hh >8  <ss hh >16  <bd >16  <bd >8  <ss hh >8  | 
 <bd >8  <bd hh >16  <bd >16  r8  <ss hh >8  <bd hh >8  <ss hh >16  <bd >16  <bd >16  <bd hh >16  <bd >8  | 
 <bd >16  <bd >16  <bd >8  <bd rb >8  <tommh hho >8  <bd cymc >8  <toml cymr >16  <bd >16  <bd hh >8  <ss hh >8  | 
 <bd >8  <ss hh >16  <tommh >16  <bd hh >8  <ss hh >8  <bd >8  <ss hh >16  <bd >16  r8  <ss hh >16  <bd >16  | 
 <bd >16  <bd hh >16  <bd hh >16  r16  <bd cymr >8  <ss hh >8  <bd >8  <toml cymr >16  <bd >16  <bd hh >8  <ss hh >8  | 
 <bd hh >8  <bd hh >16  <bd >16  <bd >8  <sn >8  <bd >8  <ss hh >16  <bd >16  <bd >16  <tommh >16  <bd hh >8  | 
 <bd >16  <bd >16  <bd >8  <bd rb >8  <ss hh >8  <bd >8  <ss hh >16  <bd >16  <bd >8  <bd rb >8  | 
 <bd >8  <ss hh >16  <bd >16  <bd >8  <toml cymr >8  <bd >8  <bd hh >16  <bd >16  r16  <bd >16  <bd >16  <bd >16  | 
 <bd hh >16  <bd >16  <ss hh >16  <bd >16  <bd cymr >8  <ss hh >8  <bd >8  <ss hh >16  <bd >16  <bd hh >8  <toml cymr >8  | 
 <bd hh >8  <ss hh >16  <bd >16  r16  r8  <tommh >16  <bd >16  <bd >8.  | 
 <tommh >8.  r16  <bd >8  <bd >8  <bd cymr >4  | 
 <sn >8.  r16 <bd hh >4  <bd >8.  r16  | 
 <bd cymr >8  <toml cymr >8  <bd >8.  <bd >16  <bd rb >16  <bd hh >16  <bd hh >16  <bd >16  | 
 <bd cymc >8.  <bd >16  <bd hh >4  <sn >8.  <bd hh >16  | 
 <bd rb >8  <sn hh >8  <bd rb >8.  <bd hh >16  <bd hh >8  <sn hh >8  | 
 <bd cymc >8  <sn hh >16  r16  <sn >16  <bd cymc >16  <bd hh >16  <bd >16  <bd >8  <bd >16  <bd >16  <bd hh >8  <sn >8  | 
 <bd rb >8.  <bd >16  <bd hh >8  <sn hh >8  <bd >8  <ss hh >16  r16  | 
 <bd hh >8  <ss hh >8  <bd hh >8.  <bd cymc >16  <bd hh >16  <bd >16  <bd hh >16  <bd hh >16  | 
 <bd rb >16  <bd >8. <bd hh >4  <bd >8.  <bd cymc >16  | 
 <bd hh >8  <sn >8  <bd >8  <bd hh >16  r16  <bd cymr >8  <toml cymr >8  <bd hh >8  <bd >16  <bd >16  | 
r16^"(three)"  r16  <bd >8  | 
 r16  <bd >16  r16  r16  <bd rb >8  <bd cymc >8  <bd cymr >8.  <bd rb >16  | 
 <bd cymr >16  <sn rb >8  <bd hh >16  <bd rb >8.  <bd cymr >16  <bd hh >8  <bd cymr >8  | 
 <bd cymr >8.  <bd cymr >16  <bd cymr >16  <bd hh >8.  | 
 <bd hh >8.  <sn hh >16  <sn >8  <bd cymr >8  <bd cymr >8.  <bd cymr >16  | 
 <sn >16  <bd hh >8.  <bd rb >8.  <bd rb >16  | 
 <bd rb >16  <bd rb >8.  r16  <bd >8.  <bd >16  <bd hh >8.  | 
 r8  r8  <sn >4  <bd hh >8.  <bd cymc >16  | 
 <bd rb >8  <sn hh >8  r8.  r16  | 
 <bd rb >8  <sn >8 <sn >8  <sn hh >16  r16  <sn >8  <toml cymr >8  <bd hh >16  <bd >16  <sn hh >16  <bd >16  | 
 <bd hh >8  <sn hh >8 <bd >8  <toml cymr >16  <bd hh >16  <bd rb >8  <ss hh >8  <bd rb >8  <ss hh >16  <bd cymc >16  | 
 <bd rb >4 <bd >8  <sn hh >16  <bd >16  <bd cymr >16  <bd >16  <bd rb >16  <bd cymc >16  r8  <bd hh >16  <bd >16  | 
 <sn >4 <bd >8.  r16  <bd hh >8  <bd hh >8  <bd hh >8  <sn >16  r16  | 
 <bd rb >8  <ss hh >8  <bd >8  <ss hh >16  <bd >16  <bd hh >16  <bd >16  <bd >16  r16  <bd hh >8  <bd cymc >16  <bd >16  | 
 <bd cymr >4  <bd >8  <ss hh >16  <bd hh >16  <bd hh >8  <sn hh >8  <bd >8.  r16  | 
 <bd hh >8  <bd >8  <bd >16  <bd rb >8  <bd hh >16  <bd hh >8  <sn >16  <bd hh >16  | 
 <bd >8  <sn >8  <sn hh >8. 
}

lyric = \lyricmode {
	One two e 'n four e 'n One two three 'n four One 'n two three 'n four 'n One two three 'n four One 'n two a e four One two 'n three four 'n One 'n two 'n three four 'n One 'n two 'n a three 'n four 'n One 'n two three e four One two three 'n four 'n a One 'n two 'n three four a One two three 'n four One 'n two three 'n a four 'n One two a three 'n four One 'n two three 'n four 'n a One two 'n three 'n four 'n a One 'n two 'n three 'n a four 'n One two 'n three 'n four 'n a 'n two 'n a 'n four e 'n a One 'n two 'n a 'n four 'n a 'n two 'n a 'n four e 'n a One 'n two 'n a three 'n four 'n a One 'n two 'n a 'n four e 'n a One 'n two 'n three 'n four 'n a 'n two 'n a three 'n four e 'n One two three 'n four 'n a One 'n two 'n a 'n four e a One 'n three 'n four 'n a 'n two 'n a three 'n four e 'n One two 'n a three 'n four 'n a One 'n two 'n a three 'n four e 'n a One 'n two 'n a three 'n four 'n a 'n two 'n a three e 'n four 'n One two a three 'n four a One 'n two three 'n four 'n a 'n two three 'n four 'n a One 'n two 'n a three 'n four e 'n a One two a three four 'n a One 'n two 'n a three e 'n four e One two a three 'n four One 'n two 'n three e four 'n One two a three 'n four a One 'n two 'n a three 'n a four e 'n One two 'n a three 'n four 'n a One 'n two 'n a three 'n a four 'n One 'n two 'n a 'n four 'n a One 'n two 'n a 'n four e 'n a One 'n two 'n a three 'n four 'n a 'n two 'n a three 'n four e 'n One 'n two 'n a three 'n four 'n a One 'n two 'n a three 'n four e 'n a 'n two 'n a three 'n four 'n a 'n two 'n a three e 'n four e 'n One 'n two 'n a three 'n four 'n a One 'n two 'n a 'n a four e 'n One 'n two 'n a three 'n four 'n a One 'n two 'n a three e 'n four e 'n One 'n two 'n a three 'n four 'n a One 'n two 'n a e 'n a four e 'n a One 'n two 'n a three 'n four 'n a a two e three four 'n One two three four One 'n two a three e 'n a four a One two a three 'n four a One 'n two 'n three e 'n a four 'n a One 'n two a three 'n four 'n One 'n two a three e 'n a four e One two a three 'n four 'n One 'n two 'n a 'n e One 'n two a three e a four a One 'n two a three e four a One 'n two a three e four a One e e three e One two a three 'n One 'n two 'n three 'n four e 'n a One 'n two 'n a three 'n four 'n a One two 'n a three e 'n a 'n a One two three 'n four 'n One 'n two 'n a three e 'n four 'n a One two 'n a three 'n four One 'n two e a three 'n a four 'n One 
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

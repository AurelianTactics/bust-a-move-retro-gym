previous_bubbles = 0
function correct_bubbles()
  if data.bubbles > previous_bubbles then
    local delta = data.bubbles - previous_bubbles
    previous_bubbles = data.bubbles
    return delta
  else
    return 0
  end
end

function done_check()
  if data.gameover == 0 then
    return true
  end
  return false
end

previous_score = 0
function correct_score ()
  local current_score = 0
  local hundreds = (data.score_hyaku % 16)*100
  local thousands = (math.floor(data.score_hyaku/16))*1000
  local ten_thousands = (data.score_man % 16)*10000
  local hundred_thousands = (math.floor(data.score_man/16))*100000
  current_score = data.score_jyuu * 10 + hundreds + thousands + ten_thousands + hundred_thousands
  if current_score > previous_score then
    local delta = current_score - previous_score
    previous_score = current_score
    return delta
  elseif previous_score - current_score > 500000 then
    --not sure what happens when you get over 1,000,000. if it resets then this catches it
	delta = 1000000 - previous_score + current_score
	previous_score = current_score
	return delta
  else
    return 0
  end
end

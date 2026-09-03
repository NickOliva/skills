-- Keep the authored page plan and keep each question with its workspace.
local page_count = 0

function Div(block)
  if block.classes:includes("problem") then
    block.content:insert(1, pandoc.RawBlock("latex", "\\par\\noindent\\begin{minipage}{\\linewidth}"))
    block.content:insert(pandoc.RawBlock("latex", "\\end{minipage}\\par\\vspace{4mm}"))
    return block.content
  end
  if block.classes:includes("practice-page") then
    page_count = page_count + 1
    if page_count > 1 then
      block.content:insert(1, pandoc.RawBlock("latex", "\\clearpage"))
    end
    return block.content
  end
end

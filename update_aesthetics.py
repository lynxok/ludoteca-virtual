import re

with open('c:/Users/astud/OneDrive/Juegos de mesa/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Enlarge modal image
html = html.replace('width: 246px; height: 300px;', 'width: 350px; height: auto; max-height: 500px; object-fit: contain;')
html = html.replace('max-width: 800px;', 'max-width: 1000px;') # Make modal wider to fit bigger image

# 2. Add game colors to drawMap
map_color_logic = """                        // Neon border
                        ctx.strokeStyle = '#0ff';
                        ctx.lineWidth = 2;
                        ctx.strokeRect(c*TILE_SIZE+2, r*TILE_SIZE+2, TILE_SIZE-4, TILE_SIZE-4);
                        
                        // Game color
                        const colors = ['#e6194B', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#42d4f4', '#f032e6', '#bfef45', '#fabed4', '#469990', '#dcbeff', '#9A6324', '#fffac8', '#800000', '#aaffc3', '#808000', '#ffd8b1', '#000075', '#a9a9a9', '#ffffff'];
                        ctx.fillStyle = colors[(tile - 10) % colors.length];
                        ctx.fillRect(c*TILE_SIZE+6, r*TILE_SIZE+6, TILE_SIZE-12, TILE_SIZE-12);"""

html = re.sub(r'// Neon border.*?ctx\.fillRect\(c\*TILE_SIZE\+10, r\*TILE_SIZE\+10, TILE_SIZE-20, TILE_SIZE-20\);', map_color_logic, html, flags=re.DOTALL)

# 3. Update drawPlayer
new_draw_player = """function drawPlayer() {
            const px = player.x * TILE_SIZE;
            const py = player.y * TILE_SIZE;
            
            ctx.shadowBlur = 0; 
            
            const dirX = player.dirX;
            const dirY = player.dirY;

            // Make Sonic 16-bit and slightly larger than a tile
            const drawX = px; 
            const drawY = py - 12; // Taller offset

            // Sonic Blue Body & Head
            ctx.fillStyle = '#0026e6';
            ctx.fillRect(drawX + 8, drawY + 2, 24, 20); // Head
            ctx.fillRect(drawX + 12, drawY + 22, 16, 14); // Body

            // Spikes (16-bit style sharper triangles)
            if (dirX === 1) { 
                ctx.beginPath(); ctx.moveTo(drawX+8, drawY+2); ctx.lineTo(drawX-4, drawY+8); ctx.lineTo(drawX+8, drawY+14); ctx.fill();
                ctx.beginPath(); ctx.moveTo(drawX+8, drawY+10); ctx.lineTo(drawX-6, drawY+16); ctx.lineTo(drawX+8, drawY+22); ctx.fill();
                ctx.beginPath(); ctx.moveTo(drawX+10, drawY+18); ctx.lineTo(drawX-2, drawY+24); ctx.lineTo(drawX+10, drawY+28); ctx.fill();
            } else if (dirX === -1) { 
                ctx.beginPath(); ctx.moveTo(drawX+32, drawY+2); ctx.lineTo(drawX+44, drawY+8); ctx.lineTo(drawX+32, drawY+14); ctx.fill();
                ctx.beginPath(); ctx.moveTo(drawX+32, drawY+10); ctx.lineTo(drawX+46, drawY+16); ctx.lineTo(drawX+32, drawY+22); ctx.fill();
                ctx.beginPath(); ctx.moveTo(drawX+30, drawY+18); ctx.lineTo(drawX+42, drawY+24); ctx.lineTo(drawX+30, drawY+28); ctx.fill();
            }

            // Face / Belly
            ctx.fillStyle = '#ffcc99';
            if (dirY === 1 || dirX !== 0) { 
                ctx.fillRect(drawX + 12, drawY + 10, 16, 12); // Snout/Face
                ctx.beginPath(); ctx.arc(drawX+20, drawY+29, 6, 0, 2*Math.PI); ctx.fill(); // Belly
            }

            // Eyes 
            if (dirY === 1) { 
                ctx.fillStyle = '#fff';
                ctx.fillRect(drawX + 13, drawY + 10, 6, 8);
                ctx.fillRect(drawX + 21, drawY + 10, 6, 8);
                ctx.fillStyle = '#000';
                ctx.fillRect(drawX + 16, drawY + 13, 3, 4);
                ctx.fillRect(drawX + 21, drawY + 13, 3, 4);
            } else if (dirX === 1) { 
                ctx.fillStyle = '#fff'; ctx.fillRect(drawX + 18, drawY + 10, 10, 8);
                ctx.fillStyle = '#000'; ctx.fillRect(drawX + 24, drawY + 13, 4, 4);
            } else if (dirX === -1) { 
                ctx.fillStyle = '#fff'; ctx.fillRect(drawX + 12, drawY + 10, 10, 8);
                ctx.fillStyle = '#000'; ctx.fillRect(drawX + 12, drawY + 13, 4, 4);
            }

            // Shoes (Red & White)
            ctx.fillStyle = '#ff0000';
            ctx.fillRect(drawX + 4, drawY + 36, 14, 10); 
            ctx.fillRect(drawX + 22, drawY + 36, 14, 10); 
            ctx.fillStyle = '#fff';
            ctx.fillRect(drawX + 10, drawY + 36, 4, 10);
            ctx.fillRect(drawX + 28, drawY + 36, 4, 10);

            // Highlight interaction target
            const tx = player.x + player.dirX;
            const ty = player.y + player.dirY;
            if(tx >=0 && tx < COLS && ty >= 0 && ty < ROWS) {
                const targetTile = map[ty][tx];
                if (targetTile >= 10) {
                    ctx.strokeStyle = '#f0f';
                    ctx.lineWidth = 2;
                    ctx.strokeRect(tx*TILE_SIZE, ty*TILE_SIZE, TILE_SIZE, TILE_SIZE);
                    
                    const gameIndex = targetTile - 10;
                    const game = gamesData[gameIndex];
                    if (game) {
                        const tooltipWidth = 180;
                        const tooltipHeight = 40;
                        const tooltipX = tx*TILE_SIZE - (tooltipWidth/2) + (TILE_SIZE/2);
                        const tooltipY = ty*TILE_SIZE - 50;

                        ctx.fillStyle = 'rgba(0, 0, 0, 0.9)';
                        ctx.fillRect(tooltipX, tooltipY, tooltipWidth, tooltipHeight);
                        ctx.strokeStyle = '#0ff';
                        ctx.lineWidth = 2;
                        ctx.strokeRect(tooltipX, tooltipY, tooltipWidth, tooltipHeight);
                        
                        ctx.fillStyle = '#ff0';
                        ctx.font = "9px 'Press Start 2P'";
                        const shortName = game.name.length > 15 ? game.name.substring(0, 14) + '..' : game.name;
                        ctx.fillText(shortName, tooltipX + 8, tooltipY + 15);
                        
                        ctx.fillStyle = '#f0f';
                        ctx.font = "8px 'Press Start 2P'";
                        ctx.fillText("[ENTER] Abrir", tooltipX + 8, tooltipY + 30);
                    }
                }
            }
        }"""

pattern = r'function drawPlayer\(\) \{.*?(?=function render\(\) \{)'
html_new = re.sub(pattern, new_draw_player + '\n\n        ', html, flags=re.DOTALL)

with open('c:/Users/astud/OneDrive/Juegos de mesa/index.html', 'w', encoding='utf-8') as f:
    f.write(html_new)

print("HTML Updated.")

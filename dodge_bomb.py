import os
import sys
import pygame as pg
import random
import time


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}  # こうかとんの移動量を示す辞書
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rect: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとん又は爆弾のRect
    戻り値：タプル（横方向判定結果、縦方向判定結果）
    画面内ならTrue/画面外ならFalse
    """
    horizon, vertical = True, True
    if rect.left < 0 or WIDTH < rect.right:  # 横方向指定
        horizon = False
    if rect.top < 0 or HEIGHT < rect.bottom:  # 縦方向指定
        vertical = False
    return horizon, vertical


def gameover(screen: pg.Surface) -> None:
    """
    引数：ゲームオーバー画面を描画したいスクリーン
    戻り値：なし
    """
    end_screen = pg.Surface((WIDTH, HEIGHT))  # ゲームオーバー画面の背景
    end_screen.set_alpha(200)  # 背景の透明度を設定
    gameover_font = pg.font.Font(None, 80)  # game overテキストのフォント設定
    gameover_txt = gameover_font.render("Game Over", True, (255, 255, 255))  # game overテキストの描画設定
    end_screen.blit(gameover_txt, (WIDTH/2 - 150, HEIGHT/2 - 50))  # テキストをblit
    crying_kk_img = pg.image.load("fig/8.png")  # 泣いているこうかとん画をロード
    end_screen.blit(crying_kk_img, (WIDTH/2 + 180, HEIGHT/2 - 60))  # テキストの右側にこうかとんを描画
    end_screen.blit(crying_kk_img, (WIDTH/2 -220, HEIGHT/2 - 60))  # テキストの左側にこうかとんを描画
    screen.blit(end_screen, (0, 0))  # 引数で指定したスクリーンにゲームオーバー画面をblit
    pg.display.update()
    time.sleep(5)
    return


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    bb_img = pg.Surface((20, 20))  # 一辺が20のsurfaceの描画
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  # 半径10の丸い赤色の爆弾の描画
    bb_img.set_colorkey((0, 0, 0))  # 爆弾の背景を透過
    bb_rct = bb_img.get_rect()  # 爆弾を動かせるようにrect化
    bb_rct.center = (random.randint(0, WIDTH), random.randint(0, HEIGHT))  # 爆弾のランダムな初期位置
    vx, vy = +5, +5  # 爆弾の初期速度

    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        if kk_rct.colliderect(bb_rct):  # kkとbbのrectが重なっていたら
            gameover(screen)
            return

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for k, tpl in DELTA.items():
            if key_lst[k]:
                sum_mv[0] += tpl[0]  # こうかとんの横方向の移動量
                sum_mv[1] += tpl[1]  # こうかとんの縦方向の移動量
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):  # こうかとんがどこかしらはみ出ているなら
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])  # 直前の動きをキャンセルする
        screen.blit(kk_img, kk_rct)

        bb_rct.move_ip(vx, vy)  # 練習2:爆弾移動
        horizon, vertical = check_bound(bb_rct)
        if not horizon:
            vx *= -1
        if not vertical:
            vy *= -1
        screen.blit(bb_img, bb_rct)  # 練習2:爆弾表示
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()

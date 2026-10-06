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


def gameover(screen: pg.Surface) -> None:  # こうかとんと爆弾が接触するとゲームオーバー画面を表示する関数
    """
    引数：ゲームオーバー画面を描画したいスクリーン
    戻り値：なし
    背景を描画しているスクリーンを指定すること
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


def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:  # 爆弾の大きさと速度が時間経過で変化する関数
    """
    引数：なし
    戻り値：タプル（異なる大きさの爆弾のリストと爆弾の速度のリスト）
    """
    bb_imgs = []

    for i in range(1, 11):
        bb_img = pg.Surface((20*i, 20*i))  # 大きさの変わる四角の描画
        pg.draw.circle(bb_img, (255, 0, 0), (10*i, 10*i), 10*i)  # 半径の変わる丸い赤色の爆弾の描画
        bb_img.set_colorkey((0, 0, 0))  # 爆弾の背景を透過
        bb_imgs.append(bb_img)  # 爆弾のサイズをリストの中に格納
    bb_accs = list(range(1, 11))  # 変化する爆弾の速度用のリスト
    return bb_imgs, bb_accs


def get_kk_imgs() -> dict[tuple[int, int], pg.Surface]:
    """
    引数：なし
    戻り値：辞書（押下キーに対する移動量の合計値タプルをキー、rotozoomしたSurfaceを値とした）
    """
    kk_img = pg.image.load("fig/3.png")
    kk_img_flip = pg.transform.flip(kk_img, True, False)
    kk_dict = {
        (0, 0): pg.transform.rotozoom(kk_img_flip, 0, 0.9),  # 何もキーが押されていない
        (5, 0): pg.transform.rotozoom(kk_img_flip, 0, 0.9),  # 右に進むとき
        (-5, 0): pg.transform.rotozoom(kk_img, 0, 0.9),  # 左に進むとき
        (0, 5): pg.transform.rotozoom(kk_img_flip, -90, 0.9),  # 下に進むとき
        (0, -5): pg.transform.rotozoom(kk_img_flip, 90, 0.9),  # 上に進むとき
        (5, 5): pg.transform.rotozoom(kk_img_flip, -45, 0.9),  # 右下に進むとき
        (-5, 5): pg.transform.rotozoom(kk_img, 45, 0.9),  # 左下に進むとき
        (5, -5): pg.transform.rotozoom(kk_img_flip, 45, 0.9),  # 右上に進むとき
        (-5, -5): pg.transform.rotozoom(kk_img, -45, 0.9),  # 左上に進むとき
    }
    return kk_dict


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    # kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_imgs = get_kk_imgs()
    kk_rct = kk_imgs[(0, 0)].get_rect()
    kk_rct.center = 300, 200

    # bb_img = pg.Surface((20, 20))  # 一辺が20のsurfaceの描画
    # pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  # 半径10の丸い赤色の爆弾の描画
    # bb_img.set_colorkey((0, 0, 0))  # 爆弾の背景を透過
    bb_imgs, bb_accs = init_bb_imgs()
    bb_rct = bb_imgs[0].get_rect()  # 爆弾を動かせるようにrect化
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
        kk_img = kk_imgs[tuple(sum_mv)]  # 移動方向からこうかとんの向きを変更
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):  # こうかとんがどこかしらはみ出ているなら
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])  # 直前の動きをキャンセルする
        screen.blit(kk_img, kk_rct)

        bb_img = bb_imgs[min(tmr//500, 9)]  # 爆弾の大きさ変更
        bb_rct.width = bb_img.get_rect().width  # 爆弾の大きさが変わったときにrectのwidthを更新
        bb_rct.height = bb_img.get_rect().height  # 爆弾の大きさが変わったときにrectのheightを更新
        avx = vx * bb_accs[min(tmr//500, 9)]  # 時間経過ごとに爆弾の横方向の速度が増加
        avy = vy * bb_accs[min(tmr//500, 9)]  # 時間経過ごとに爆弾の縦方向の速度が増加
        bb_rct.move_ip(avx, avy)  # 練習2:爆弾移動
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

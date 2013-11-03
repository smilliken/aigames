#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <stdint.h>
#include <time.h>
#include <sys/time.h>

#define debugf(args...) fprintf(stderr, args)

#define fi(A, B) for (i = (A); i < (B); ++i)
#define ff(A, B) for (f = (A); f < (B); ++f)

typedef uint64_t u64;
static inline u64 tm() {
    struct timeval tv;
    gettimeofday(&tv, 0);
    return tv.tv_sec*1000000ULL + tv.tv_usec;
}

struct pos {
    struct pos *parent;
    struct pos *children[7];
    char board[6][7];
    int winner;
    double w, n;
};

static inline void free_pos(struct pos *p) {
    int f;
    if (p) ff(0, 7) free_pos(p->children[f]);
}

void debug_pos(struct pos *p) {
    int i, f;
    debugf("POS %p\n", p);
    debugf("%p\n", p->parent);
    fi(0, 7) debugf("%p%c", p->children[i], (i < 6 ? ' ' : '\n'));
    fi(0, 6) {
        ff(0, 7) {
            debugf("%c", p->board[i][f]["0.X"+1]);
        }
        debugf("\n");
    }
    debugf("%d\n", p->winner);
    debugf("%lf %lf/%lf\n\n", p->w/p->n, p->w, p->n);
}

const double C = 1.41421356237; // sqrt(2)
static inline double calc_score(double t, struct pos *p, int sign) {
    double frac = (((sign-1)/-2)*p->n + sign*p->w) / p->n;
    int rough_log;
    frexp(t, &rough_log);
    return frac + C*sqrt(rough_log/p->n);
}

static inline int winner(struct pos *p, int ci, int cf) {
    int i, f;
    char acc, (*b)[7] = p->board, c = b[ci][cf];

    acc = 1;
    for (i = ci+1; i < 6 && b[i][cf] == c; ++i) acc += 1;
    for (i = ci-1; i >= 0 && b[i][cf] == c; --i) acc += 1;
    if (acc >= 4) return c;

    acc = 1;
    for (f = cf+1; f < 7 && b[ci][f] == c; ++f) acc += 1;
    for (f = cf-1; f >= 0 && b[ci][f] == c; --f) acc += 1;
    if (acc >= 4) return c;

    acc = 1;
    for (i=ci+1, f=cf+1; i<6 && f<7 && b[i][f]==c; ++i, ++f) acc += 1;
    for (i=ci-1, f=cf-1; i>=0 && f>=0 && b[i][f]==c; --i, --f) acc += 1;
    if (acc >= 4) return c;

    acc = 1;
    for (i=ci+1, f=cf-1; i<6 && f>=0 && b[i][f]==c; ++i, --f) acc += 1;
    for (i=ci-1, f=cf+1; i>=0 && f<7 && b[i][f]==c; --i, ++f) acc += 1;
    if (acc >= 4) return c;

    return 0;
}

static inline int make_move(struct pos *p, int f, int sign) {
    int i;
    fi(0, 6) if (!p->board[i][f]) {
        p->board[i][f] = sign;
        return i;
    }
    return -1;
}

static inline void unmake_move(struct pos *p, int f) {
    int i;
    fi(0, 6) if (p->board[5-i][f]) { p->board[5-i][f] = 0; return; }
}

static inline int monte_carlo_round(struct pos *p, int sign) {
    int i, f, w = 0, offset, tmp, shuffle[7];
    ff(0, 7) shuffle[f] = f;
    ff(0, 7) {
        offset = rand()%(7-f);
        tmp = shuffle[f+offset];
        shuffle[f+offset] = shuffle[f];
        shuffle[f] = tmp;
        if ((i = make_move(p, shuffle[f], sign)) != -1) {
            w = winner(p, i, shuffle[f]);
            if (!w) w = monte_carlo_round(p, -sign);
            unmake_move(p, shuffle[f]);
            break;
        }
    }
    return w;
}

static inline void estimate_score(struct pos *p, int sign) {
    int w, pw, pn;
    if ((w = (p->winner ? p->winner : monte_carlo_round(p, sign)))) {
        pw = (w == 1); pn = 1;
    } else {
        pw = 1; pn = 2;
    }
    do { p->w += pw; p->n += pn; } while ((p = p->parent));
}

static inline void add_leaf_node(struct pos *parent, int f, int sign) {
    int i;
    struct pos *p = malloc(sizeof(*p));
    parent->children[f] = p;

    memset(p, 0, sizeof(*p));
    p->parent = parent;
    memcpy(p->board, parent->board, sizeof(p->board));
    if ((i = make_move(p, f, sign)) != -1) {
        p->winner = winner(p, i, f);
        estimate_score(p, -sign);
    } else {
        p->winner = -sign;
    }
}

static inline void update(struct pos *p, int sign) {
    int f, best_f = 0;
    double score, best_score;
    struct pos *c, *parent;

    while (p && !p->winner) {
        best_score = -INFINITY;
        ff(0, 7) {
            c = p->children[f];
            score = c ? calc_score(p->n, c, sign) : INFINITY;
            if (score >= best_score) {
                best_score = score;
                best_f = f;
            }
        }
        parent = p;
        p = p->children[best_f];
        sign *= -1;
    }
    p ? estimate_score(p, sign) : add_leaf_node(parent, best_f, -sign);
}

static inline struct pos *new_root(struct pos *root, int move) {
    struct pos *tmp = root->children[move];
    tmp->parent = 0;
    root->children[move] = 0;
    free_pos(root);
    return tmp;
}

int main(void) {
    int f, move = 0;
    u64 start;
    double score, best_score;
    char c, buf[5]; // go!\n\0
    struct pos *tmp, *root = malloc(sizeof(*root));

    srand(time(0));
    memset(root, 0, sizeof(*root));

    while (fgets(buf, 5, stdin)) {
        start = tm();
        c = buf[0];
        if ('0' <= c && c <= '6' && buf[1] == '\n' && !buf[2]) {
            move = c-'0';
            if (root->children[move]) {
                root = new_root(root, move);
            } else {
                ff(0, 7) if (root->children[f]) {
                    free_pos(root->children[f]);
                    root->children[f] = 0;
                }
                root->w = root->n = root->winner = 0;
                if (make_move(root, move, -1) == -1) {
                    goto err;
                }
            }
        } else if (strcmp(buf, "go!\n")) {
            goto err;
        }

        if (root->winner) return 0;

        while (tm() - start < 1000000ULL - 5000ULL) {
            update(root, 1);
        }

        best_score = -INFINITY;
        ff(0, 7) if ((tmp = root->children[f])) {
            score = tmp->w / tmp->n;
            if (score >= best_score) {
                best_score = score;
                move = f;
            }
        }
        if (root->children[move]) {
            printf("%d\n", move);
            fflush(stdout);
            root = new_root(root, move);
        } else {
            goto err;
        }
    }

    free_pos(root);
    return 0;

 err:
    debugf("Invalid input: %s\n", buf);
    return 1;
}

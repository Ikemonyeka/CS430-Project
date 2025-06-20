def minimize_cost(shopping_list, prices, promotions):
    item_ids = sorted(shopping_list.keys())
    init_state = tuple(shopping_list[i] for i in item_ids)

    promo_vectors = []
    for promo in promotions:
        vec = tuple(promo['items'].get(i, 0) for i in item_ids)
        if any(vec):
            promo_vectors.append((vec, promo['price'], promo['items']))

    memo = {}

    def dp(state):
        if state in memo:
            return memo[state]

        if all(q == 0 for q in state):
            memo[state] = (0, [], state)
            return memo[state]

        # No promotion case
        no_promo_cost = sum(q * prices[i] for i, q in zip(item_ids, state))
        best = (no_promo_cost, [], state)

        # Try promotions
        for vec, promo_price, promo_items in promo_vectors:
            new_state = []
            for need, take in zip(state, vec):
                if take > need:
                    break
                new_state.append(need - take)
            else:
                sub_cost, sub_promos, _ = dp(tuple(new_state))
                total = promo_price + sub_cost
                if total < best[0]:
                    best = (total, sub_promos + [promo_items], tuple(new_state))

        memo[state] = best
        return best

    total_cost, promos_used, final_state = dp(init_state)

    # put together remaining items
    remaining = {i: q for i, q in zip(item_ids, final_state) if q > 0}
    return total_cost, promos_used, remaining, sum(prices[i] * q for i, q in remaining.items())

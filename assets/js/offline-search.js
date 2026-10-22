(function ($) {
  'use strict';

  $(function () {
    const $inputs = $('.td-search-input');
    if (!$inputs.length) return;

    let pages;
    let loadError = false;
    $.getJSON($inputs.first().data('offline-search-index-json-src'))
      .done((data) => { pages = data; $inputs.trigger('change'); })
      .fail(() => { loadError = true; $inputs.trigger('change'); });

    const english = document.documentElement.lang === 'en';
    const labels = english
      ? { heading: 'Search results', empty: 'No results found', error: 'Search index could not be loaded' }
      : { heading: '搜索结果', empty: '未找到结果', error: '搜索索引加载失败' };

    $inputs.closest('form').on('submit', (event) => event.preventDefault());
    $inputs.on('input change', function () {
      const $input = $(this);
      const query = $input.val().trim().toLocaleLowerCase();
      $input.popover('dispose');
      if (!query) return;

      const $results = $('<div>');
      if (loadError) {
        $results.text(labels.error);
      } else if (!pages) {
        return;
      } else {
        const terms = query.split(/\s+/);
        const matches = pages
          .filter((page) => /\/(?:v\d+\.\d+\/)?en\//.test(page.ref) === english)
          .map((page) => {
            const title = page.title.toLocaleLowerCase();
            const description = page.description.toLocaleLowerCase();
            const body = page.body.toLocaleLowerCase();
            if (!terms.every((term) => title.includes(term) || description.includes(term) || body.includes(term))) return null;
            const score = terms.reduce((total, term) => total +
              (title === term ? 100 : title.includes(term) ? 50 : 0) +
              (description.includes(term) ? 10 : 0) +
              (body.includes(term) ? 1 : 0), 0);
            return { page, score };
          })
          .filter(Boolean)
          .sort((a, b) => b.score - a.score)
          .slice(0, Number($input.data('offline-search-max-results')) || 10);

        if (!matches.length) $results.text(labels.empty);
        matches.forEach(({ page }) => {
          $('<div class="mb-3">')
            .append($('<a class="d-block">').attr('href', page.ref).text(page.title))
            .append($('<small class="text-muted">').text(page.excerpt))
            .appendTo($results);
        });
      }

      const $content = $('<div>')
        .append($('<strong>').text(labels.heading))
        .append($('<button type="button" class="close" aria-label="Close">').text('×'))
        .append($('<div class="mt-2 offline-search-list">').append($results));
      $input.popover({
        html: true,
        placement: 'bottom',
        trigger: 'manual',
        content: $content[0],
        template: '<div class="popover offline-search-result" role="tooltip"><div class="arrow"></div><div class="popover-body"></div></div>'
      }).popover('show');
      $('.offline-search-result .close').on('click', () => {
        $input.val('').popover('dispose');
      });
    });
  });
})(jQuery);

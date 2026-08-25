---
title: "Schedule"
permalink: /schedule/
---

The schedule below is tentative and will be updated as the semester progresses.

<table class="course-schedule">
  <thead>
    <tr>
      <th>Date</th>
      <th>Topic</th>
      <th>Lead</th>
      <th>Assignment</th>
      <th>Slides</th>
    </tr>
  </thead>
  <tbody>
    {%- for row in site.data.schedule %}
    <tr>
      <td class="schedule-date">{{ row.date }}</td>
      <td>{{ row.topic }}</td>
      <td class="schedule-lead">{{ row.lead }}</td>
      <td>{{ row.assignment | markdownify | remove: "<p>" | remove: "</p>" | strip }}</td>
      <td>{{ row.reading }}</td>
      <td>{{ row.slides | markdownify }}</td>
    </tr>
    {%- endfor %}
  </tbody>
</table>
